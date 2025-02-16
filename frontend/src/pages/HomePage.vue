<template>
  <div class="body">
     <h1>The Main Page</h1>
  </div>
  
  
</template>

<script lang="ts">
  import { defineComponent } from "vue";
import { useUserStore } from "../stores/user";
import { useUsersStore } from "../stores/users";
  

  //This home page will display user lists of books
  //It will also display the recommended books
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
       
      },
      methods: {
          
         
      }, 
      computed: {
        user() {
              const userStore = useUserStore;
              return this.userStore.user; // Bind to the fetched user data from Pinia store
          },
   
    
      },
      setup() {
          const userStore = useUserStore();
    
          const usersStore = useUsersStore();
  
          return { userStore , usersStore };
      },
  });
  </script>


<style scoped>
  .body{
      font-family: Arial, Helvetica, sans-serif;
      display: grid;
      grid-template-columns: auto auto;
      grid-template-rows: 10% 30% 20% 30% 10%;
      gap: 1rem 0.25rem;
  }
  #profile-box{
      grid-column: 1;
      grid-row: 1/span 2;
  }

  #hobby{
    grid-column: 1;
      grid-row: 3;

  }

  #create-hobby{
      grid-column: 1;
      grid-row: 4;
      padding-top: 0.5rem;
  }
  #create-hobby>h3{
      text-align: center;
      background-color: #D9D9D9;
  }
  #create-hobby>input{
      margin-bottom: 1.5rem;
  }
  .friend-accepted{

      background-color: #D9D9D9;
      grid-column: 2;
      grid-row: 1/span 2;
      padding-bottom: 2em;
  }
  .friend-pending{
   
      background-color: #D9D9D9;
      grid-column: 2;
      grid-row: 3/span 2;
  }
  .body > div{
      background-color: #659A78;
      margin:2em;
      padding:2em;
  }

  a{
      background-color: #659A78;
      margin:0.5em;
      text-decoration: none;
      color:black;
      padding: 0.2em;
  }

  a:hover, button:hover{
      color:white;
  }

  .hobbies{
      background-color: #B4DABA;
  }

  h2, .friends, div>p {
      background-color: #D9D9D9;
      margin:0.2em;
  }
  h6{
      text-align: center;
  }
  li{
      display:flex;
  }

  button{
      background-color:  #B4DABA;
      font-size: 1rem;
      margin-bottom: 0.5rem;
      border: none;
  }

</style>
