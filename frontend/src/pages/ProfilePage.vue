<template>
    <div class="body">
       <div id="profile-box">
          <h2>Welcome {{ user.first_name }}</h2>
              <p>
              Username: {{ user.username }}
              
              
              
              
          </p>
          
            <p>
                <span v-if="!editFirstName">First Name: {{ user.first_name }}</span>
                    <span v-else>
                        First Name:
                        <input v-model="editedUser.first_name" type="text" />
                    </span>
                    <button v-if="!editFirstName" @click="toggleEditField('FirstName')">Edit</button>
                    <button v-else @click="saveField('first_name')">Save</button>
            </p>
            
            <p>
                <span v-if="!editLastName">Last Name: {{ user.last_name }}</span>
                    <span v-else>
                        Last Name:
                        <input v-model="editedUser.last_name" type="text" />
                    </span>
                    <button v-if="!editLastName" @click="toggleEditField('LastName')">Edit</button>
                    <button v-else @click="saveField('last_name')">Save</button>
            </p>
            <p>
                <span v-if="!editEmail">Email: {{ user.email }}</span>
                <span v-else>
                    Email:
                    <input v-model="editedUser.email" type="email" />
                </span>
                <button v-if="!editEmail" @click="toggleEditField('Email')">Edit</button>
                <button v-else @click="saveField('email')">Save</button>
            </p>
            <p>
            <span v-if="!editDateOfBirth">Date of Birth: {{ user.date_of_birth }}</span>
                <span v-else>
                    {{ user.date_of_birth }}
                    <input v-model="editedUser.date_of_birth" type="date" />
                </span>
                <button v-if="!editDateOfBirth" @click="toggleEditField('DateOfBirth')">Edit</button>
                <button v-else @click="saveField('date_of_birth')">Save</button>
            </p>
     
           
      </div>
    </div>
    
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { User } from "../types/index";
    import { useUserStore } from "../stores/user";
    import { useUsersStore } from "../stores/users";
    import VueCookies from 'vue-cookies';
  
    
  
  
    export default defineComponent({
        data() {
            return {
            editFirstName: false,
            editLastName: false,
            editEmail: false,
            editDateOfBirth: false,
            
            editedUser: {
                first_name: "",
                last_name: "",
                email: "",
                date_of_birth: "",                
            },
            user_id : Number(window.sessionStorage.getItem("user_id")),

            
            };
        },
        async mounted() {
            try {
                console.log("Fetching fresh user data...");
                const userId = Number(window.sessionStorage.getItem("user_id"));
                const user = await this.userStore.fetchUserReturn(userId);
                this.userStore.user = user; // Ensure store is updated with new data
                console.log("Updated User:", this.userStore.user);
            } catch (error) {
                console.error("Error fetching user:", error);
            }
        },
        methods: {
            toggleEditField(field: string) {
              console.log(typeof field)
                this[`edit${field}`] = !this[`edit${field}`];
                if (this[`edit${field}`]) {
                    this.editedUser[field.toLowerCase()] = this.user[field.toLowerCase()];
                }
                //this.editPassword = !this.editPassword; // Toggle edit mode
            },
            
            async saveField(field: string) {
               
                try {
                    
                    const payload = {
                        [field.toLowerCase()]: this.editedUser[field.toLowerCase()],
                    };
                    console.log(payload)
                    const response = await fetch(`http://localhost:8000/site_user/${this.user.id}/`, {
                        method: "PUT",
                        headers: {
                            'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                            'Content-Type': 'application/json',
                            'X-CSRFToken': VueCookies.get('csrftoken'),
                        },
                        credentials: 'include',
                        body: JSON.stringify(payload),
                    });
                
                    console.log("CSRF Token:", this.userStore.csrf);
  
                    if (!response.ok) {
                        throw new Error("Failed to update field");
                    }
  
                    const updatedUser = await response.json();
                    console.log(updatedUser)
                    this.userStore = this.userStore.saveUsers(updatedUser); // Update the user state in the store
                    console.log("Reloading...");
                    window.location.reload(true);
                
                    alert(`${field} updated successfully!`);
                } catch (error) {
                    console.error(error);
                    alert(`Failed to update ${field}.`);
                }
            }, 
  
        }, 
        computed: {
            user() {
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
  