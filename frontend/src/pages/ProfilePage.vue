<template>
    <div class="body">
       <div id="profile-box">
          <h2>Welcome {{ user.first_name }}</h2>
              <p>Username: {{ user.username }} </p>
          
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

     <!-- Toggle Buttons -->
 
    <!-- Accepted Friends Section -->
    <div v-if="activeTab === 'accepted'" class="friend-accepted">
        <!-- Toggle Buttons -->
        <button @click="activeTab = 'accepted'" class="chosenButton">Accepted Friends</button>
        <button @click="activeTab = 'pending'">Pending Friends</button>
        <div>
            <h2>Accepted Friends</h2>
        </div>
        <ul v-for="(friendship, index) in friendships.filter(friendship => friendship.user === user.id && friendship.accepted)" :key="index" class="friends">
            <li>
                {{ friendship.username }}
                <button @click="deleteFriendship(friendship.id)">Delete</button>
            </li>
        </ul>
    </div>

    <!-- Pending Friends Section -->
    <div v-if="activeTab === 'pending'" class="friend-pending">
        <!-- Toggle Buttons -->
        <button @click="activeTab = 'accepted'">Accepted Friends</button>
        <button @click="activeTab = 'pending'" class="chosenButton">Pending Friends</button>
        <div>
            <h2>Pending Friends</h2>
        </div>
        <ul v-for="(friendship, index) in friendships.filter(friendship => friendship.user === user.id && !friendship.accepted)" :key="index" class="friends">
            <li>
                {{ friendship.username }}
                <button @click="acceptFriendship(friendship.id)">Accept</button>
                <button @click="deleteFriendship(friendship.id)">Delete</button>
            </li>
        </ul>
    </div>       
    
    </div>
    
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { User, Friendship} from "../types/index";
    import { useUserStore } from "../stores/user";
    import { useUsersStore } from "../stores/users";
    import { useFriendshipsStore } from "../stores/friendships";
    import VueCookies from 'vue-cookies';
  
    
  
  
    export default defineComponent({
        data() {
            return {
            editFirstName: false,
            editLastName: false,
            editEmail: false,
            editDateOfBirth: false,
            activeTab: "accepted", // Default to Accepted Friends

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

            //fetch all the friendships
            let responseFriendship = await fetch("http://localhost:8000/friendships/");
            let dataFriendship = await responseFriendship.json();
            let friendships = dataFriendship.friendships as Friendship[];
    
            const storeFriendships = useFriendshipsStore();
            storeFriendships.saveFriendships(friendships);
            console.log(storeFriendships)
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
            
            // Accepts the pending friendship between user and friend it then makes an accepted friendship between friend and user
           //This means the friendship is symmetrical 
           async acceptFriendship(friendshipId: number) {
              try {
                  const acceptResponse = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
                      method: "PUT",
                      headers: {
                          "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                          "Content-Type": "application/json",
                          "X-CSRFToken": VueCookies.get("csrftoken"),
                      },
                      credentials: "include",
                  });

                  if (!acceptResponse.ok) {
                      throw new Error("Failed to accept friendship.");
                  }

                  const dataAccept = await acceptResponse.json();
                  const newAccept = dataAccept.friendship as Friendship;

                  // Update the friendship in the store
                  const friendshipsStore = useFriendshipsStore();
                  friendshipsStore.addFriendship(newAccept);
                  window.location.reload();
                  alert(`Accepted successfully!`);
              } catch (error) {
                  console.error("Error accepting friendship:", error);
                  alert("Failed to accept friendship. Please try again.");
              }
          },
          //rejects the friendships between users and friend whether pending or accepted
          async deleteFriendship(friendshipId: number) {
            try {
              const response = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
                method: "DELETE",
                headers: {
                  "Authorization": `Bearer ${VueCookies.get("access_token")}`,
                  "Content-Type": "application/json",
                  "X-CSRFToken": VueCookies.get("csrftoken"),
                },
                credentials: "include",
              });

              if (!response.ok) {
                throw new Error("Failed to delete friendship");
              }

              //Remove the deleted friendship from the store
              const friendshipsStore = useFriendshipsStore();
              friendshipsStore.removeFriendship(friendshipId);

              window.location.reload();
              alert("Friendship deleted successfully!");
            } catch (error) {
              console.error("Error deleting friendship:", error);
              alert("Failed to delete friendship. Please try again.");
            }
          },

  
        }, 
        computed: {
            user() {
                return this.userStore.user; // Bind to the fetched user data from Pinia store
            },

            friendships(){
              const friendshipsStore = useFriendshipsStore;
              return this.friendshipsStore.friendships;
          },

        },
        setup() {
            const userStore = useUserStore();
            const usersStore = useUsersStore();
            const friendshipsStore = useFriendshipsStore();
            return { userStore , usersStore , friendshipsStore };
        },
    });
    </script>
  
  
  <style scoped>
    .body{
        font-family: Arial, Helvetica, sans-serif;
        display: flex;
    }

    .body > div{
        background-color: #2f4a54;
        margin:2em;
        padding:2em;
    }

     .chosenButton{
        background-color: white;
        color:black;   
    }

    .friends{
        background-color: #2f4a54;
        padding:0.5em;
    }
  
    a{
        background-color: #2f4a54;
        margin:0.5em;
        text-decoration: none;
        color:black;
        padding: 0.2em;
    }
  
    a:hover, button:hover{
        color:grey;
    }
  
    h2, div>p {
        background-color: #71929f;
        margin:0.2em;
        color: white;
    }
    h6{
        text-align: center;
    }

    li{
        color: white;
        style:none;
    }

    li>button{
        background-color: #71929f;
        margin-left: 0.5em;
    }
  
    button{
        background-color:  #2f4a54;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        border: none;
        color: white;
        border-style:ridge;
    }
  
  </style>
  