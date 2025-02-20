<template>
    <section>
        <h2>Your Books:</h2> 
    </section>
    <h3>Currently Reading</h3>
    <section  class="display">
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'READING' && book.user === user_id)" :key="index">
            <router-link :to="`/book/${userBook.book}`" class="book-link">
                <p>Title: {{ books[userBook.book - 1]?.title }}</p>
                <p>Author: {{ books[userBook.book - 1]?.author }}</p>
            </router-link>
        </div>
    </section>
    <h3>WishList</h3>
    <section class="display">
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'WISHLIST' && book.user === user_id)" :key="index">
            <router-link :to="`/book/${userBook.book}`" class="book-link">
                <p>Title: {{ books[userBook.book - 1]?.title }}</p>
                <p>Author: {{ books[userBook.book - 1]?.author }}</p>
            </router-link>
        </div>
    </section>
    <h3>Completed</h3>
    <section class="display">
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'COMPLETED' && book.user === user_id)" :key="index">
            <router-link :to="`/book/${userBook.book}`" class="book-link">
                <p>Title: {{ books[userBook.book - 1]?.title }}</p>
                <p>Author: {{ books[userBook.book - 1]?.author }}</p>
            </router-link>
        </div>
    </section>
</template>
  
<script lang="ts">
  import { defineComponent } from "vue";
 
  import { User , Book , UserBook} from "../types/index.ts";
  import {useUsersStore} from "../stores/users.ts"
  import {useBooksStore} from "../stores/books.ts"
  import {useUserBooksStore} from "../stores/userBooks.ts"
  import VueCookies from 'vue-cookies';

  
  export default defineComponent({
    data() {
        return{
            user_id : Number(window.sessionStorage.getItem("user_id")),
        }
    
    },
  
    async mounted() {
      let response = await fetch("http://localhost:8000/site_users/");
      let data = await response.json();
      let users = data.users as User[];
      const store = useUsersStore()
      store.saveUsers(users)

      let responseBook = await fetch("http://localhost:8000/books/");
      let dataBook = await responseBook.json();
      let books = dataBook.books as Book[];
      const storeBook = useBooksStore()
      storeBook.saveBooks(books)

      let responseUserBook = await fetch("http://localhost:8000/user_books/");
      let dataUserBook = await responseUserBook.json();
      let userBooks = dataUserBook.user_books as UserBook[];
      const storeUserBook = useUserBooksStore()
      storeUserBook.saveUserBooks(userBooks)  
  
    },
  
    computed: {
        books(){
              const storeBook = useBooksStore();
              return this.storeBook.books;
        },
        userBooks(){
            const storeUserBook = useUserBooksStore();
            return this.storeUserBook.userBooks;
        },
      
    },
  
    methods: {
      
      },
      setup() {
            const storeBook = useBooksStore();
            const storeUserBook = useUserBooksStore();
            return {storeBook , storeUserBook};
    
        },
    },
      
           
  
  
  );
  </script>
  
  <style scoped>
    .body{
        font-family: Arial, Helvetica, sans-serif;
    }

    div{
        background-color: #2f4a54;
        margin:0.2em;
        padding:0.2em;
    }

    h2, h3, div>p, .book-link>p {
        background-color: #71929f;
        margin:0.2em;
    }

    h2, h3, div>p{
        color: white;
    }
    .book-link{
        text-decoration: none;
        color: white;
    }

    .book-link:hover {
        color: grey;
    }

    .display{
        display: flex;
    }
  
  
  </style>
  