<template>
  <AuthorNavBarComponent />
  <div class="body">
    <!-- Book Info Section - Author can edit this -->
    <div id="profile-box">
      <h2>Book Info</h2>
        <!-- Display cover image if available -->
        <div v-if="book.cover_image">
        <img :src="`http://localhost:8000/${book.cover_image}`" alt="Book Cover" />
      </div>
      <p v-else>No cover image available</p>
      <p v-for="field in editableFields" :key="field.key">
        <span v-if="!field.isEditing">{{ field.label }}: {{ book[field.key] }}</span>
        <span v-else>
          {{ field.label }}:
          <input v-model="editedBook[field.key]" :type="field.type" />
        </span>
        <button v-if="!field.isEditing" @click="toggleEditField(field.key)">Edit</button>
        <button v-else @click="saveField(field.key)">Save</button>
      </p>

      <p>Rating: {{ averageRating }}</p>

      <!-- Genres List -->
      <div>
        <h3>Genres:</h3>
        <ul>
          <li v-for="genre in bookGenresForThisBook" :key="genre.id">
            {{ genre.type }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Review Section -->
    <section id="review-box">
      <h2>Reviews</h2>
      <div class="reviews-container">
        <div
          v-for="(review, index) in reviews.filter(review => review.book === book.id)"
          :key="index"
        >
          <p>Title: {{ review.title }}</p>
          <p>Username: {{ review.username }}</p>
          <p>Rating: {{ review.rating }} Stars</p>
          <p>Message: {{ review.message }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import AuthorNavBarComponent from "../components/AuthorNav.vue";
import { defineComponent } from "vue";
import { useBookStore } from "../stores/book";
import { useReviewsStore } from "../stores/reviews";
import { useRoute } from "vue-router";
import {useCookies} from "vue3-cookies";
import { useUserBooksStore } from "../stores/userBooks";

export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),
      //for editing the book
      editableFields: [
        { key: "title", label: "Title", type: "text", isEditing: false },
        { key: "author", label: "Author", type: "text", isEditing: false },
        { key: "blurb", label: "Blurb", type: "text", isEditing: false },
        { key: "isbn", label: "ISBN", type: "text", isEditing: false },
      ],
      editedBook: {} as Record<string, string>,
      //fetch genres
      bookGenres: [] as { book: number; genre: number }[],
      genres: [] as { id: number; type: string }[],
    };
  },
  async mounted() {
    const route = useRoute();
    //fetch book info
    const bookId = parseInt(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id); 

    await this.bookStore.fetchBookReturn(bookId); 


    // Fetch reviews
    const responseReview = await fetch("http://localhost:8000/reviews/");
    const dataReview = await responseReview.json();
    const storeReview = useReviewsStore();
    storeReview.saveReviews(dataReview.reviews);

    // Fetch book_genre relationships
    const bookGenresResponse = await fetch("http://localhost:8000/book_genres/");
    const bookGenresData = await bookGenresResponse.json();
    this.bookGenres = bookGenresData.book_genre;

    // Fetch all genres
    const genresResponse = await fetch("http://localhost:8000/genres/");
    const genresData = await genresResponse.json();
    this.genres = genresData.genres ?? genresData;
  },
  components: {
    AuthorNavBarComponent,
  },
  computed: {
    book() {
      return this.bookStore.book;
    },
    reviews() {
      const storeReview = useReviewsStore();
      return storeReview.reviews;
    },
    //calculate rating
    averageRating() {
      const bookReviews = this.reviews.filter(
        (review) => review.book === this.book.id
      );
      if (bookReviews.length === 0) return "No ratings yet";
      const total = bookReviews.reduce((sum, review) => sum + review.rating, 0);
      return (total / bookReviews.length).toFixed(1) + " Stars";
    },
    //get the genres for this book
    bookGenresForThisBook() {
      return this.bookGenres
        .filter((bg) => bg.book === this.book.id)
        .map((bg) => this.genres.find((g) => g.id === bg.genre))
        .filter((g) => g !== undefined);
    },
  },
  methods: {
    //toggle field to edit mode
    toggleEditField(fieldKey: string) {
      const field = this.editableFields.find((f) => f.key === fieldKey);
      if (field) {
        field.isEditing = !field.isEditing;
        if (field.isEditing) {
          this.editedBook[fieldKey] = this.book[fieldKey];
        }
      }
    },
    //save changes and edit the field using put method
    async saveField(fieldKey: string) {
      try {
        const { cookies } = useCookies(); 
        const payload = { [fieldKey]: this.editedBook[fieldKey] };
        const response = await fetch(
          `http://localhost:8000/book/${this.book.id}/`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${cookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": cookies.get("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) throw new Error("Failed to update field");

        this.bookStore.saveBooks(await response.json());
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert(`Failed to update ${fieldKey}.`);
      }
    },
  },
  setup() {
    const bookStore = useBookStore();
    const storeReview = useReviewsStore();
    const storeUserBook = useUserBooksStore();
    return { bookStore, storeReview, storeUserBook };
  },
});
</script>


<style scoped>
/* Book Info Section */
#profile-box {
  flex: 1;
  min-width: 300px;
  background-color: #2f4a54; 
  color: white; 
  padding: 1.5em; 
  margin: 1em;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s ease, transform 0.3s ease;
  max-height: 70vh; 
  overflow-y: auto;   
}



#profile-box h2 {
  text-align: center;
  background-color: #6a8b91; 
  padding: 10px;
  border-radius: 5px;
  color: white; 
  font-size: 1.5rem;
}


#profile-box p {
  font-size: 1rem;
  color: white; 
  margin: 0.5em 0;
  background-color: #527a8a;
  padding: 0.2rem;
  border-radius: 8px;
  margin-bottom: 0.5em;
  box-shadow: 1px 1px 6px rgba(0, 0, 0, 0.1);
}



/* Review Section */
#review-box {
  flex: 2;
  min-width: 400px;
  background-color: #2f4a54;
  padding: 1.5em; 
  margin: 1em;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s ease, transform 0.3s ease;
  max-height: 70vh; 
  overflow: hidden; 
}



#review-box h2 {
  text-align: center;
  background-color: #6a8b91;
  padding: 10px;
  border-radius: 5px;
  color: white;
  font-size: 1.5rem;
}

/* Scrollable container for reviews */
.reviews-container {
  max-height: calc(100% - 60px);  
  overflow-y: auto;  
  padding-right: 15px; 
  box-sizing: border-box; 
}

/* Review Cards */
#review-box > .reviews-container > div {
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
  transition: transform 0.2s ease-in-out;
}

#review-box > .reviews-container > div {
  background-color: white;
}




/* Modal Styling */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 350px; /* Reduced width */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-content input,
.modal-content textarea,
.modal-content select {
  width: 100%;
  padding: 10px;
  margin: 0.5rem 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.modal-content button {
  margin-top: 1rem;
  background-color: #4b6c6f;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #5d7f82;
}

.modal-content button:active {
  background-color: #4b6c6f;
}

/* General Body Styling */
.body {
  display: flex;
  justify-content: space-between;
  margin: 2rem;
}

/* Ensure the content in modal is vertically centered */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

input,
textarea,
select {
  font-size: 1rem;
}

h2 {
  font-size: 1.5rem;
}

button {
  cursor: pointer;
}

button:focus {
  outline: none;
}

/* Genre Section */
#profile-box ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

#profile-box li {
  background-color: #6a8b91;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.2s ease;
}

#profile-box li:hover {
  background-color: #81a4aa;
  transform: scale(1.05);
  cursor: default;
}

/* Styling for book cover image */
#profile-box img {
  width: 100%; 
  height: 300px; 
  max-width: 350px; 
  object-fit: cover; 
  border-radius: 10px; 
}

/* Media query for smaller screens */
@media (max-width: 768px) {
  /* On mobile screens, make the image smaller and adapt */
  #profile-box img {
    max-width: 100%; 
    height: 300px; 
  }

  .body{
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  #profile-box {
    height: 400vh; 
    overflow-y: auto;   
  }
}

/* Media query for very small screens */
@media (max-width: 480px) {
  /* Ensure image fits within smaller containers */
  #profile-box img {
    max-width: 90%; 
  }
}



</style>
