<template>
    <div class="body">
       <div id="profile-box">
          <h2>User Info</h2>
          <p>Username: {{ reader.username}}</p>
       
           <button @click="addFriendship(reader.id)" v-if="hasFriendship === null">Request</button>
           <div v-else>
                <p v-if="hasFriendship === true">FOLLOWING</p>
                <p v-else>REQUESTED</p>
                <router-link :to="`/message/${reader.id}`" class="message-link"> Message </router-link>
           </div>
       </div>

 
        <div class="display-books">
        <h2>Wishlist</h2>
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'WISHLIST' && book.user === reader.id)" 
                :key="index"
                class="book-container">
                <router-link :to="`/book/${userBook.book}`" class="book-link">
                    <p class="book-title">Title: {{ books[userBook.book - 1]?.title }}</p>
                    <p class="book-author">Author: {{ books[userBook.book - 1]?.author }}</p>
                </router-link>
            
        </div>

        <h2>Reading</h2>
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'READING' && book.user === reader.id)" 
                :key="index"
                class="book-container">
                <router-link :to="`/book/${userBook.book}`" class="book-link">
                    <p class="book-title">Title: {{ books[userBook.book - 1]?.title }}</p>
                    <p class="book-author">Author: {{ books[userBook.book - 1]?.author }}</p>
                </router-link>
            
        </div>
        <h2>Completed</h2>
        <div v-for="(userBook, index) in userBooks.filter(book => book.status === 'COMPLETED' && book.user === reader.id)" 
                :key="index"
                class="book-container">
                <router-link :to="`/book/${userBook.book}`" class="book-link">
                    <p class="book-title">Title: {{ books[userBook.book - 1]?.title }}</p>
                    <p class="book-author">Author: {{ books[userBook.book - 1]?.author }}</p>
                </router-link>
            
        </div>
       </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import { useReaderStore } from "../stores/reader.ts";

import { useRoute } from "vue-router";
import VueCookies from "vue-cookies";
import { Reader, Friendship } from "../types";
import { useFriendshipsStore } from "../stores/friendships";
import {useBooksStore} from "../stores/books.ts"
import {useUserBooksStore} from "../stores/userBooks.ts"


export default defineComponent({
    data() {
        return {
            reader_id: Number(window.sessionStorage.getItem("reader_id")),

        };
    },
    async mounted() {
        //gets the user information 
        const route = useRoute();
        const readerId = parseInt(route.params.id);
        let reader = await this.readerStore.fetchReaderReturn(readerId);

        //fetch all the friendships
        let responseFriendship = await fetch("http://localhost:8000/friendships/");
        let dataFriendship = await responseFriendship.json();
        let friendships = dataFriendship.friendships as Friendship[];
        const storeFriendships = useFriendshipsStore();
        storeFriendships.saveFriendships(friendships);
        console.log(storeFriendships)

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
    methods: {
        async addFriendship(friend_id: number) {
            console.log(friend_id)
            const payload = {
            user_id: this.reader_id,
            friend_id: friend_id,
            accepted: false,
            };
            console.log(payload);

            const friendshipResponse = await fetch(`http://localhost:8000/friendships/`, 
            {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': VueCookies.get('csrftoken'),
            },
            credentials: 'include',
            body: JSON.stringify(payload),
            });

            // Add the newly created friendship to Pinia store 
            const data = await friendshipResponse.json();
            let createdFriendship = data.friendship as Friendship;

            const friendshipsStore = useFriendshipsStore();
            friendshipsStore.addFriendship(createdFriendship);

            window.location.reload();
            alert(`Friendship requested successfully!`);
        },

        
    },
    computed: {
        reader() {
            return this.readerStore.reader;
        },
        friendships(){
            return this.friendshipsStore.friendships;
        },
        hasFriendship() {
            const friendship = this.friendships.find(friendship => 
            friendship.friend === this.reader.id && friendship.user === this.reader_id
            );
            return friendship ? friendship.accepted : null; // Returns `true`, `false`, or `null`
        },
        books() {
            const storeBook = useBooksStore();
            return this.storeBook.books;
        },
        userBooks() {
            const storeUserBook = useUserBooksStore();
            return this.storeUserBook.userBooks;
        },
        
    },
    setup() {
        const readerStore = useReaderStore();
        const friendshipsStore = useFriendshipsStore();
        const storeBook = useBooksStore();
        const storeUserBook = useUserBooksStore();
        return { readerStore , friendshipsStore, storeBook, storeUserBook };
    }
});
</script>
  
  <style scoped>
    .body {
    font-family: Arial, Helvetica, sans-serif;
    display: flex;
    flex-wrap: wrap;
    gap: 1.5em;
    padding: 1.5em;
    background-color: #EFE0CB; /* Light background */
}

/* Profile Box */
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

/* User Info Text */
#profile-box p {
    font-size: 1rem;
    color: #cfd8dc;
    margin: 0.6rem 0;
}

/* FOLLOWING / REQUESTED status */
#profile-box div p {
    font-size: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.5rem;
}

#profile-box div p:first-of-type {
    background-color: #71929f; /* Muted blue */
    color: white;
}

#profile-box div p:last-of-type {
    background-color: #4d707d; /* Subtle gray-blue */
    color: white;
}

/* Button Container (Stacked Buttons) */
.button-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
    margin-top: 1rem;
}

/* Buttons */
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

/* Message Link */
.message-link {
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

/* Book Display */
.display-books {
    flex-grow: 1;
    background-color: #2f4a54;
    padding: 1.5em;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

/* Section Titles */
h2 {
    background-color: #1e363f;
    padding: 0.6em;
    border-radius: 6px;
    color: white;
    text-align: center;
    margin-bottom: 1em;
    font-size: 1.1rem;
}

/* Individual Book Container */
.book-container {
    background-color: #3b5d67;
    padding: 1em;
    margin-bottom: 1em;
    border-radius: 6px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease-in-out, box-shadow 0.3s ease;
}

/* Different background colors for books */
.book-container:nth-child(odd) {
    background-color: #456b75; /* Darker blue-green */
}

.book-container:nth-child(even) {
    background-color: #527a85; /* Lighter blue */
}

/* Hover effect for books */
.book-container:hover {
    transform: scale(1.03);
    box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.25);
}

/* Book Link */
.book-link {
    display: block;
    text-decoration: none;
    color: white;
    font-size: 1rem;
    font-weight: bold;
    transition: transform 0.2s ease-in-out;
}

/* Book Title & Author */
.book-title {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.3rem;
}

.book-author {
    font-size: 0.9rem;
    color: #cfd8dc;
}

/* List Items */
li {
    list-style: none;
    color: white;
    font-size: 1rem;
    margin-bottom: 0.4rem;
}

li > button {
    background-color: #4d707d;
    margin-left: 0.3em;
    border-radius: 3px;
}

h6 {
    text-align: center;
    color: #e0f2f1;
    font-size: 0.9rem;
}

  </style>
  
  