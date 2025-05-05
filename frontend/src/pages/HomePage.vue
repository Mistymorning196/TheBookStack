<template>
  <ReaderNavBarComponent />
  <div class="body">
    <h1>Homepage</h1>
  </div>

  <!-- Display recommended books -->
  <h2>Recommended Books:</h2>
  <section class="display">
    <div v-for="(book, index) in recommendedBooks" :key="index">
      <router-link :to="`/book/${book.id}`" class="book-link">
        <div v-if="book.cover_image">
          <img :src="`http://localhost:8000/${book.cover_image}`" alt="Book Cover" class="book-cover"/>
        </div>
        <p v-else>No cover image available</p>
        <p>Title: {{ book.title }}</p>
        <p>Author: {{ book.author }}</p>
      </router-link>
    </div>
  </section>
   <!-- Takes you to all books page -->
  <button @click="goToAllBooks" class="go-to-all-books-button">See All Books</button>

    <!-- Display recommended readers -->
  <h2>Recommended Readers:</h2>
  <section class="display">
    <div v-for="(reader, index) in recommendedReaders" :key="index">
      <router-link :to="`/user/${reader.id}`" class="user-link">
        <p>Username: {{ reader.username }}</p>
      </router-link>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { useReadersStore } from "../stores/readers";
import { useBooksStore } from "../stores/books";
import { Book, Reader, Friendship, ReaderGenre, UserBook, Genre } from "../types/index";

export default defineComponent({
  data() {
    return {
      reader_id: null as number | null,
      recommendedBooks: [] as Book[],
      recommendedReaders: [] as Reader[],
    };
  },
  async mounted() {
    //fetch cookies from login
    const sessionCookie = document.cookie.split(';');
    let currentSessionid = '';
    for (let cookie of sessionCookie) {
      cookie = cookie.trim();
      if (cookie.startsWith("sessionid=")) {
        currentSessionid = cookie.substring("sessionid=".length);
      }
    }

    const previousSessionid = window.sessionStorage.getItem("session_id");
    if (currentSessionid === previousSessionid) {
      this.reader_id = Number(window.sessionStorage.getItem("reader_id"));
    } else {
      const params = new URLSearchParams(window.location.search);
      this.reader_id = parseInt(params.get("u") || "0");
      sessionStorage.setItem("reader_id", this.reader_id.toString());
      sessionStorage.setItem("session_id", currentSessionid);
    }

    await this.fetchDataAndRecommend();
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    // This async function fetches data from various endpoints and generates book and reader recommendations
    async fetchDataAndRecommend() {
      // Fetch all required data in parallel
      const [
        bookRes, readerRes, bookGenreRes,
        readerGenreRes, userBooksRes, friendshipRes
      ] = await Promise.all([
        fetch("http://localhost:8000/books/"),
        fetch("http://localhost:8000/readers/"),
        fetch("http://localhost:8000/book_genres/"),
        fetch("http://localhost:8000/reader_genres/"),
        fetch("http://localhost:8000/user_books/"),
        fetch("http://localhost:8000/friendships/")
      ]);

      // Parse the JSON responses
      const books = (await bookRes.json()).books as Book[];
      const readers = (await readerRes.json()).readers as Reader[];
      const bookGenres = (await bookGenreRes.json()).book_genre || [];
      const readerGenres = (await readerGenreRes.json()).reader_genre || [];
      const userBooks = (await userBooksRes.json()).user_books || [];
      const friendships = (await friendshipRes.json()).friendships || [];

      // Save books and readers to the stores
      useBooksStore().saveBooks(books);
      useReadersStore().saveReaders(readers);

      // Build the current reader's genre preference vector
      const currentReaderVector: Record<number, number> = {};
      for (const rg of readerGenres) {
        if (rg.user === this.reader_id) {
          currentReaderVector[rg.genre] = rg.count;
        }
      }

      // Create a set of book IDs already read by the current reader
      const userBookIds = new Set(
        userBooks.filter((ub: UserBook) => ub.user === this.reader_id).map((ub: UserBook) => ub.book)
      );

      // Score all books the reader hasn't read using content-based filtering
      const bookScores: { book: Book; score: number }[] = [];
      for (const book of books) {
        if (userBookIds.has(book.id)) continue;

        // Build the genre vector for the book
        const genreVector: Record<number, number> = {};
        for (const bg of bookGenres) {
          if (bg.book === book.id) {
            genreVector[bg.genre] = (genreVector[bg.genre] || 0) + 1;
          }
        }

        // Compute dot product as a similarity score between reader and book
        let score = 0;
        for (const genre in genreVector) {
          score += (currentReaderVector[+genre] || 0) * genreVector[+genre];
        }

        bookScores.push({ book, score });
      }

      // Build reader vectors for collaborative filtering
      const readerVectors: Record<number, Record<number, number>> = {};
      for (const rg of readerGenres) {
        if (!readerVectors[rg.user]) readerVectors[rg.user] = {};
        readerVectors[rg.user][rg.genre] = rg.count;
      }

      // Compute cosine similarity between the current reader and all others
      const readerSimilarities: { readerId: number; similarity: number }[] = [];
      for (const readerId in readerVectors) {
        const id = Number(readerId);
        if (id === this.reader_id) continue;

        const otherVector = readerVectors[id];
        let dotProduct = 0, currentNorm = 0, otherNorm = 0;

        const allGenres = new Set([...Object.keys(currentReaderVector), ...Object.keys(otherVector)].map(Number));
        for (const genre of allGenres) {
          const a = currentReaderVector[genre] || 0;
          const b = otherVector[genre] || 0;
          dotProduct += a * b;
          currentNorm += a * a;
          otherNorm += b * b;
        }

        // Avoid divide-by-zero and compute similarity
        const similarity = (Math.sqrt(currentNorm) * Math.sqrt(otherNorm)) === 0
          ? 0
          : dotProduct / (Math.sqrt(currentNorm) * Math.sqrt(otherNorm));

        readerSimilarities.push({ readerId: id, similarity });
      }

      // Select top 5 similar readers with a positive similarity
      const topSimilarReaders = readerSimilarities
        .sort((a, b) => b.similarity - a.similarity)
        .slice(0, 5)
        .filter(item => item.similarity > 0)
        .map(item => item.readerId);

      // Count books from similar readers not read by the current reader
      const recommendedBooksFromSimilarReaders: Record<number, number> = {};
      for (const userBook of userBooks) {
        if (topSimilarReaders.includes(userBook.user) && !userBookIds.has(userBook.book)) {
          recommendedBooksFromSimilarReaders[userBook.book] = (recommendedBooksFromSimilarReaders[userBook.book] || 0) + 1;
        }
      }

      // Map the recommended books with their occurrence count
      const collaborativeBookScores = Object.entries(recommendedBooksFromSimilarReaders)
        .map(([bookId, count]) => {
          const book = books.find(b => b.id === Number(bookId));
          return book ? { book, count } : null;
        })
        .filter(Boolean) as { book: Book; count: number }[];

      // Sort collaborative filtering results by popularity among similar readers
      const sortedCollaborativeBooks = collaborativeBookScores
        .sort((a, b) => b.count - a.count)
        .map(item => item.book);

      // Exclude friends from reader recommendations
      const excludedReaderIds = new Set(
        friendships.filter((f: Friendship) => f.user === this.reader_id).map((f: Friendship) => f.friend)
      );

      // Score other readers by genre similarity
      const readerScores: { reader: Reader; score: number }[] = [];
      for (const reader of readers) {
        if (reader.id === this.reader_id || excludedReaderIds.has(reader.id)) continue;

        const readerVector: Record<number, number> = {};
        for (const rg of readerGenres) {
          if (rg.user === reader.id) {
            readerVector[rg.genre] = rg.count;
          }
        }

        let score = 0;
        for (const genre in readerVector) {
          score += (currentReaderVector[+genre] || 0) * readerVector[+genre];
        }

        readerScores.push({ reader, score });
      }

      // If current reader has genre preferences, use hybrid recommendation
      const currentReaderHasPrefs = Object.keys(currentReaderVector).length > 0;

      if (currentReaderHasPrefs) {
        // Combine top content-based and collaborative books, avoiding duplicates
        const contentBasedBooks = bookScores
          .sort((a, b) => b.score - a.score)
          .map(item => item.book);

        const combinedBooks: Book[] = [];
        const seenIds = new Set<number>();
        for (const book of [...contentBasedBooks, ...sortedCollaborativeBooks]) {
          if (!seenIds.has(book.id)) {
            combinedBooks.push(book);
            seenIds.add(book.id);
          }
          if (combinedBooks.length >= 5) break;
        }

        this.recommendedBooks = combinedBooks;

        // Recommend top 5 readers based on genre similarity
        this.recommendedReaders = readerScores
          .sort((a, b) => b.score - a.score)
          .slice(0, 5)
          .map(item => item.reader);

      } else {
        // Fallback for new users: recommend popular books and diverse readers

        // Count how often each book appears in genres
        const bookCounts: Record<number, number> = {};
        for (const bg of bookGenres) {
          bookCounts[bg.book] = (bookCounts[bg.book] || 0) + 1;
        }

        // Recommend top 5 most common books
        this.recommendedBooks = books
          .map(book => ({ book, count: bookCounts[book.id] || 0 }))
          .sort((a, b) => b.count - a.count)
          .slice(0, 5)
          .map(item => item.book);

        // Recommend readers with the most diverse genre interests
        const readerDiversity = readers
          .filter(r => r.id !== this.reader_id && !excludedReaderIds.has(r.id))
          .map(reader => {
            const genres = readerGenres.filter((rg: ReaderGenre) => rg.user === reader.id);
            const uniqueGenres = new Set(genres.map((g: Genre) => g.genre));
            return { reader, diversity: uniqueGenres.size };
          })
          .sort((a, b) => b.diversity - a.diversity)
          .slice(0, 5)
          .map(item => item.reader);

        this.recommendedReaders = readerDiversity;
      }
    },


    goToAllBooks() {
      this.$router.push('/allBooks');
    }
  }
});
</script>




<style scoped>
/* Body Styling */
.body {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #EFE0CB; 
    margin: 0;
    padding: 0.8rem; 
    max-height: 75vh;
    overflow-y: auto; 
}

/* Heading Styling */
h1, h2 {
    color: white;
    background-color: #2f4a54;
    padding: 0.3rem 1rem; 
    margin: 0.3rem 0; 
    border-radius: 5px;
    font-size: 1.6rem; 
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
}

h1 {
    font-size: 1.8rem;
    margin-top: 1rem;
}

h2 {
    font-size: 1.4rem;
    margin-top: 0.3rem; 
}

/* Display Section (Book and User Lists) */
.display {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    justify-content: center; 
    margin-top: 1rem;
    padding: 0 1rem; 
}

/* General Card Styling for Book and User Items */
.display > div {
    background-color: #2f4a54;
    padding: 0.5rem; 
    margin: 0.3rem; 
    border-radius: 8px;
    flex-basis: 30%; 
    max-width: 250px; 
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); 
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.display > div:hover {
    transform: translateY(-4px); 
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); 
}

/* Link Styling */
.book-link, .user-link {
    text-decoration: none;
    color: white;
    font-size: 0.9rem; 
    font-weight: bold;
    transition: color 0.3s ease, transform 0.3s ease;
}

/* Hover Effect for Links */
.book-link:hover, .user-link:hover {
    color: #f0b400; 
    transform: scale(1.03); 
}

/* Paragraph Styling (inside links) */
.book-link > p, .user-link > p {
    margin: 0.2rem 0;
    padding: 0.3rem;
    background-color: #71929f; 
    border-radius: 5px;
    color: white;
    text-align: center;
    font-size: 0.8rem; 
}

.all-books-button {
    background-color: #2f4a54; 
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    margin: 1rem auto 0;
    display: block;
}

.all-books-button:hover {
    background-color: #f0b400; 
    color: #2f4a54;
    transform: scale(1.03);
}

.book-cover {
  width: 60px;          
  height: 60px;          
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  margin-bottom: 0.3rem;
}

.book-cover:hover {
  transform: scale(1.03);
}



/* Additional Responsive Styling */
@media (max-width: 768px) {
    .display {
        flex-direction: column;
        align-items: center;
    }

    .display > div {
        flex-basis: 80%; 
        max-width: 100%; 
    }

    h1, h2 {
        font-size: 1.4rem; 
    }

    .book-link, .user-link {
        font-size: 0.8rem; 
    }

    .book-link > p, .user-link > p {
        font-size: 0.7rem; 
    }
}
</style>

