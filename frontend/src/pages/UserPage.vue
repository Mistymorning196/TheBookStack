<template>
  <ReaderNavBarComponent />
     <!--Display user info-->
  <div class="body">
    <div id="profile-box">
      <h2>User Info</h2>
      <p>Username: {{ reader.username }}</p>
         <!--Shows friend status-->
      <button @click="addFriendship(reader.id)" v-if="hasFriendship === null">Request</button>
      <div v-else>
        <p v-if="hasFriendship === true">FOLLOWING</p>
        <p v-else>REQUESTED</p>
      </div>
         <!--Link to message them-->
      <router-link :to="`/message/${reader.id}`" class="message-link">Message</router-link>
    </div>
       <!--Display the user's books-->
    <div class="display-books">
      <h2>Wishlist</h2>
      <div class="book-scroll-container">
        <div v-for="(userBook, index) in filteredBooks('WISHLIST')" :key="index" class="book-container">
          <router-link :to="`/book/${userBook.book}`" class="book-link">
            <p class="book-title">Title: {{ userBook.title }}</p>
            <p class="book-author">Author: {{ userBook.author }}</p>
          </router-link>
        </div>
      </div>

      <h2>Reading</h2>
      <div class="book-scroll-container">
        <div v-for="(userBook, index) in filteredBooks('READING')" :key="index" class="book-container">
          <router-link :to="`/book/${userBook.book}`" class="book-link">
            <p class="book-title">Title: {{ userBook.title }}</p>
            <p class="book-author">Author: {{ userBook.author }}</p>
          </router-link>
        </div>
      </div>

      <h2>Completed</h2>
      <div class="book-scroll-container">
        <div v-for="(userBook, index) in filteredBooks('COMPLETED')" :key="index" class="book-container">
          <router-link :to="`/book/${userBook.book}`" class="book-link">
            <p class="book-title">Title: {{ userBook.title }}</p>
            <p class="book-author">Author: {{ userBook.author }}</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useReaderStore } from "../stores/reader";
import { useRoute } from "vue-router";
import { useCookies } from "vue3-cookies"; 
import { Friendship, UserBook } from "../types";
import { useFriendshipsStore } from "../stores/friendships";
import { useBooksStore } from "../stores/books";
import { useUserBooksStore } from "../stores/userBooks";

export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),
    };
  },
  async mounted() {
    //fetch reader
    const route = useRoute();
    const readerId = parseInt(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id); 

    await this.readerStore.fetchReaderReturn(readerId); 

    //fetch friendships
    const responseFriendship = await fetch("http://localhost:8000/friendships/");
    const dataFriendship = await responseFriendship.json();
    const friendships = dataFriendship.friendships as Friendship[];
    useFriendshipsStore().saveFriendships(friendships);

    //fetch userBooks
    const responseUserBook = await fetch("http://localhost:8000/user_books/");
    const dataUserBook = await responseUserBook.json();
    const userBooks = dataUserBook.user_books as UserBook[];
    useUserBooksStore().saveUserBooks(userBooks);
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    //method to create friendship for user using post
    async addFriendship(friend_id: number) {
      const { cookies } = useCookies(); 

      const payload = {
        user_id: this.reader_id,
        friend_id: friend_id,
        accepted: false,
      };

      const accessToken = cookies.get("access_token");
      const csrfToken = cookies.get("csrftoken");

      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };

      if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
      }
      if (csrfToken) {
        headers["X-CSRFToken"] = csrfToken;
      }

      const friendshipResponse = await fetch("http://localhost:8000/friendships/", {
        method: "POST",
        headers,
        credentials: "include",
        body: JSON.stringify(payload),
      });

      const data = await friendshipResponse.json();
      const createdFriendship = data.friendship as Friendship;
      useFriendshipsStore().addFriendship(createdFriendship);

      window.location.reload();

    },
    //make sure books displayed are users
    filteredBooks(status: string) {
      return this.userBooks.filter(
        (book) => book.status === status && book.user === this.reader.id
      );
    },
  },
  computed: {
    reader() {
      return this.readerStore.reader;
    },
    friendships() {
      return this.friendshipsStore.friendships;
    },
    hasFriendship() {
      const friendship = this.friendships.find(
        (friendship) => friendship.friend === this.reader.id && friendship.user === this.reader_id
      );
      return friendship ? friendship.accepted : null;
    },
    userBooks() {
      return this.storeUserBook.userBooks;
    },
  },
  setup() {
    return {
      readerStore: useReaderStore(),
      friendshipsStore: useFriendshipsStore(),
      storeBook: useBooksStore(),
      storeUserBook: useUserBooksStore(),
    };
  },
});
</script>


  
  <style scoped>
  /*styles*/
  .body {
    font-family: Arial, Helvetica, sans-serif;
    display: flex;
    flex-wrap: wrap;
    gap: 1.5em;
    padding: 1.5em;
    background-color: #efe0cb;
  }
  
  /*info styles*/
  #profile-box {
    background-color: #2f4a54;
    color: white;
    padding: 1.5em;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
    max-width: 300px;
    width: 100%;
  }
  
  #profile-box h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: white;
    border-bottom: 2px solid #71929f;
    padding-bottom: 0.4rem;
  }
  
  #profile-box p {
    font-size: 1rem;
    color: #cfd8dc;
    margin: 0.6rem 0;
  }
  
  #profile-box div p {
    font-size: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.5rem;
  }
  
  #profile-box div p:first-of-type {
    background-color: #71929f;
    color: white;
  }
  
  #profile-box div p:last-of-type {
    background-color: #4d707d;
    color: white;
  }
  
  /*button styling*/
  button {
    background-color: #4d707d;
    font-size: 0.9rem;
    padding: 0.5em 1.2em;
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    transition: transform 0.2s ease, background 0.3s ease-in-out;
    width: 100%;
  }
  
  button:hover {
    background-color: #5e8a97;
    transform: scale(1.05);
  }
  
  .message-link {
    margin-top: 0.5em;
    display: inline-block;
    padding: 0.5em 1em;
    background-color: #4d707d;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.9rem;
    font-weight: bold;
    transition: transform 0.2s ease-in-out;
    text-align: center;
    width: 100%;
  }
  
  .message-link:hover {
    background-color: #5e8a97;
    transform: scale(1.05);
  }

  /*book display styles*/  
  .display-books {
    flex-grow: 1;
    background-color: #2f4a54;
    padding: 1.5em;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  }
  
  h2 {
    background-color: #1e363f;
    padding: 0.6em;
    border-radius: 6px;
    color: white;
    text-align: center;
    margin-bottom: 1em;
    font-size: 1.1rem;
  }
  
  .book-scroll-container {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    gap: 1rem;
    padding-bottom: 1rem;
  }
  
  .book-scroll-container::-webkit-scrollbar {
    height: 8px;
  }
  
  .book-scroll-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
  }
  
  .book-scroll-container::-webkit-scrollbar-track {
    background: #2f4a54;
  }
  
  .book-container {
    background-color: #3b5d67;
    padding: 1em;
    border-radius: 6px;
    min-width: 200px;
    flex-shrink: 0;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease-in-out, box-shadow 0.3s ease;
  }
  
  .book-container:hover {
    transform: scale(1.03);
    box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.25);
  }
  
  .book-link {
    display: block;
    text-decoration: none;
    color: white;
    font-size: 1rem;
    font-weight: bold;
  }
  
  .book-title {
    font-size: 1rem;
    margin-bottom: 0.3rem;
  }
  
  .book-author {
    font-size: 0.9rem;
    color: #cfd8dc;
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
  </style>
  