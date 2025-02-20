<template>
  <div class="body">
     <h1>The Main Page</h1>
  </div>
  <h2>Books:</h2>
  <section  class="display">
        <div v-for="(book, index) in books" :key="index">
            <router-link :to="`/book/${book.id}`" class="book-link">
                <p>Title: {{ book.title }}</p>
                <p>Author: {{ book.author }}</p>
            </router-link>
        </div>
    </section>
  <h2>Users:</h2>
  <section  class="display">
        <div v-for="(site_user, index) in site_users" :key="index">
            
                <p>Username: {{ site_user.username }}</p>
            
        </div>
    </section>
  
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { useUserStore } from "../stores/user";
    import { useUsersStore } from "../stores/users";
    import { useBooksStore } from "../stores/books"
    import { Book, User } from "../types/index";
    

    //This home page will display user lists of books
    //It will also display the recommended books and recommended users 
    export default defineComponent({
        async mounted() {
            // Fetching csrf token using session cookie information on mount
            const sessionCookie = (document.cookie).split(';');
            let currentSessionid: string = ''
            console.log(sessionCookie)
            // Checking in UserStore with CSRF token
            for (let cookie of sessionCookie) {
                cookie = cookie.trim();
                console.log(cookie)
                if (cookie.startsWith("sessionid" + "=")) {
                    currentSessionid = cookie.substring("sessionid".length + 1);
                }
            }
            
            const previousSessionid : string | null = window.sessionStorage.getItem("session_id")
            // Loading values from user store if sessionId matches
            if(currentSessionid == previousSessionid){
                const userId = Number(window.sessionStorage.getItem("user_id"));
                try {
                    const userCookie = await this.userStore.fetchUserReturn(Number(window.sessionStorage.getItem("user_id")));
                    console.log("Fetched User:", userCookie);
                } catch (error) {
                    console.error("Error fetching user:", error);
                }
            
                console.log('checked sesh')
            }
            else{
                // Extracting user id from url query
                const params = new URLSearchParams(window.location.search);
                const userId: number = parseInt(params.get("u") || "0");
                console.log(userId)
                // Fetch user data using url query information on mount
                let user = await this.userStore.fetchUserReturn(userId);
                console.log(user)
                this.userStore.user = user;
                // Set session variable
                sessionStorage.setItem("user_id", userId.toString());
                
                // Fetching csrf token using session cookie information on mount
                const session_cookie = (document.cookie).split(';');
                console.log(session_cookie)

                //Update user state in UserStore with CSRF token
                for (let cookie of session_cookie) {
                    cookie = cookie.trim();
                    console.log(cookie)
                    if (cookie.startsWith("csrftoken" + "=")) {
                        this.userStore.setCsrfToken(cookie.substring("csrftoken".length + 1));

                        console.log(this.userStore.csrf)
                    }
                    //Update sessionStorage state in UserStore with CSRF token
                    console.log(cookie)
                    if (cookie.startsWith("sessionid" + "=")) {
                        // Set session variable
                        let sessionId = cookie.substring("csrftoken".length + 1);
                        sessionStorage.setItem("session_id", sessionId);
                    }
                }
            }

            //gets all of the books
            let responseBook = await fetch("http://localhost:8000/books/");
            let dataBook = await responseBook.json();
            let books = dataBook.books as Book[];
            const storeBook = useBooksStore()
            storeBook.saveBooks(books)

            //gets all of the users
            let responseUser = await fetch("http://localhost:8000/site_users/");
        
            let dataUser = await responseUser.json();
        
            let site_users = dataUser.site_users as User[];
            console.log(site_users)
            const usersStore = useUsersStore()
            usersStore.saveUsers(site_users)

        
        },
        methods: {
            
            
        }, 
        computed: {
            site_users() {
                const usersStore = useUsersStore;
                return this.usersStore.users; // Bind to the fetched user data from Pinia store
            },
            books(){
                const storeBook = useBooksStore();
                return this.storeBook.books;
            },
    
        
        },
        setup() {
            const userStore = useUserStore();
            const usersStore = useUsersStore();
            const storeBook = useBooksStore();
    
            return { userStore , usersStore, storeBook };
        },
    });
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

    h2, h1, div>p{
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
