<template>
  <ReaderNavBarComponent />
  <div class="body">
    <div class="top-section">
      <!-- Profile Box -->
      <div id="profile-box">
        <h2>Welcome {{ reader.first_name }}</h2>
        <p>Username: {{ reader.username }} <button> <a href="http://localhost:8000/updateUser/"> Change Username </a> </button></p>

        <p v-for="field in editableFields" :key="field.key">
          <span v-if="!field.isEditing">{{ field.label }}: {{ reader[field.key] }}</span>
          <span v-else>
            {{ field.label }}:
            <input v-model="editedReader[field.key]" :type="field.type" />
          </span>
          <button v-if="!field.isEditing" @click="toggleEditField(field.key)">Edit</button>
          <button v-else @click="saveField(field.key)">Save</button>
        </p>

        <button> <a href="http://localhost:8000/updatePass/"> Change Password </a> </button>
      </div>

      <!-- Connections Box for friends including toggle -->
      <div id="connections-box">
        <h2>Connections</h2>
        <div class="tabs">
          <div class="tab-group">
            <button @click="activeTab = 'following'" :class="{ chosenButton: activeTab === 'following' }">Following</button>
            <button @click="activeTab = 'requested'" :class="{ chosenButton: activeTab === 'requested' }">Requested</button>
          </div>

          <div class="tab-group">
            <button @click="activeTabFollowers = 'followers'" :class="{ chosenButton: activeTabFollowers === 'followers' }">Followers</button>
            <button @click="activeTabFollowers = 'pending'" :class="{ chosenButton: activeTabFollowers === 'pending' }">Pending</button>
          </div>
        </div>

        <div class="connections-grid">
          <div v-if="activeTab === 'following'" class="connections-card">
            <h3>Following</h3>
            <ul>
              <li v-for="(friendship, index) in filteredFollowing" :key="index">
                <router-link :to="`/user/${friendship.friend}`">
                  <span>{{ friendship.friendUsername }}</span>
                </router-link>
                <button @click="deleteFriendship(friendship.id)">Unfollow</button>
              </li>
            </ul>
          </div>

          <div v-if="activeTab === 'requested'" class="connections-card">
            <h3>Requested</h3>
            <ul>
              <li v-for="(friendship, index) in filteredRequested" :key="index">
                <router-link :to="`/user/${friendship.friend}`">
                  <span>{{ friendship.friendUsername }}</span>
                </router-link>
                <button @click="deleteFriendship(friendship.id)">Cancel Request</button>
              </li>
            </ul>
          </div>

          <div v-if="activeTabFollowers === 'followers'" class="connections-card">
            <h3>Followers</h3>
            <ul>
              <li v-for="(friendship, index) in filteredFollowers" :key="index">
                <router-link :to="`/user/${friendship.user}`">
                  <span>{{ friendship.userUsername }}</span>
                </router-link>
                <button @click="deleteFriendship(friendship.id)">Remove</button>
              </li>
            </ul>
          </div>
          <div v-if="activeTabFollowers === 'pending'" class="connections-card">
            <h3>Pending Followers</h3>
            <ul>
              <li v-for="(friendship, index) in filteredPending" :key="index">
                <router-link :to="`/user/${friendship.user}`">
                  <span>{{ friendship.userUsername }}</span>
                </router-link>
                <button @click="acceptFriendship(friendship.id)">Accept</button>
                <button @click="deleteFriendship(friendship.id)">Remove</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section">
       <!-- Book Count Section -->
    <div class="book-count-display">
      <div class="book-count-badge">
        <span>{{ reader.book_count }}</span> Books Read
      </div>
      <div class="book-count-progress">
        <div class="progress-bar" :style="{ width: bookProgressWidth + '%' }"></div>
      </div>
      <p v-if="reader.book_count > 0" class="milestone-message">{{ bookMilestone }}</p>
    </div>

    <!-- Goals Section -->
    <div class="goals-section">
      <h3>Your Reading Goals</h3>
      <ul>
        <li v-for="(goal, index) in goals" :key="index">
          <span v-if="!goal.isEditing">Goal {{ index + 1 }}: {{ goal.value }}</span>
          <span v-else>
            Goal {{ index + 1 }}:
            <input type="number" v-model.number="goal.value" />
          </span>
          <button @click="toggleGoalEdit(index)">
            {{ goal.isEditing ? 'Save' : 'Edit' }}
          </button>
        </li>
      </ul>
    </div>
  </div>

    </div>
   
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useReaderStore } from "../stores/reader";
import { useFriendshipsStore } from "../stores/friendships";
import { useCookies } from "vue3-cookies"; 


export default defineComponent({
  data() {
    return {
      //edit data
      editableFields: [
        { key: "first_name", label: "First Name", type: "text", isEditing: false },
        { key: "last_name", label: "Last Name", type: "text", isEditing: false },
        { key: "email", label: "Email", type: "email", isEditing: false },
        { key: "date_of_birth", label: "Date of Birth", type: "date", isEditing: false },
      ],
      editedReader: {} as Record<string, string>,

      //toggle friends
      activeTab: "following",
      activeTabFollowers: "followers",

      reader_id: Number(window.sessionStorage.getItem("reader_id")),

      //goals data
      goals: [
        { key: "goal_one", value: 0, isEditing: false },
        { key: "goal_two", value: 0, isEditing: false },
        { key: "goal_three", value: 0, isEditing: false },
        { key: "goal_four", value: 0, isEditing: false },
        { key: "goal_five", value: 0, isEditing: false },
      ],
    };
  },
  async mounted() {
    try {
      //fetch user info
      const readerId = this.reader_id;

      const reader = await this.readerStore.fetchReaderReturn(readerId);
      if (reader) {
        this.readerStore.reader = reader;

        this.goals.forEach(goal => {
          goal.value = this.reader[goal.key];
        });
      }

    } catch (error) {
      console.error("Error fetching user:", error);
    }

    //fetch friendships
    const response = await fetch("http://localhost:8000/friendships/");
    const data = await response.json();
    this.friendshipsStore.saveFriendships(data.friendships);
  },
  components: {
    ReaderNavBarComponent,
  },
  computed: {
    reader() {
      return this.readerStore.reader;
    },
    friendships() {
      return this.friendshipsStore.friendships;
    },
    //get specific friends
    filteredFollowing() {
      return this.friendships.filter(f => f.user === this.reader.id && f.accepted === true);
    },
    filteredRequested() {
      return this.friendships.filter(f => f.user === this.reader.id && f.accepted === false);
    },
    filteredFollowers() {
      return this.friendships.filter(f => f.friend === this.reader.id && f.accepted === true);
    },
    filteredPending() {
      return this.friendships.filter(f => f.friend === this.reader.id && f.accepted === false);
    },
    //calculate milestones
    bookMilestone() {
      const milestones = [this.reader.goal_one, this.reader.goal_two, this.reader.goal_three, this.reader.goal_four, this.reader.goal_five];
      const currentCount = this.reader.book_count;
      const nextMilestone = milestones.find(m => m > currentCount);
      if (nextMilestone) {
        return `You're ${nextMilestone - currentCount} books away from your next milestone of ${nextMilestone} books! Keep going! 🎉`;
      }
      return "You've reached an incredible milestone! Keep reading! 📚";
    },
    //create progress bar
    bookProgressWidth() {
      const milestones = [this.reader.goal_one, this.reader.goal_two, this.reader.goal_three, this.reader.goal_four, this.reader.goal_five];
      const currentCount = this.reader.book_count;
      const nextMilestone = milestones.find(m => m > currentCount);
      if (nextMilestone) {
        return Math.min((currentCount / nextMilestone) * 100, 100);
      }
      return 100;
    },
  },
  methods: {
    //toggle fields to editable
    toggleEditField(fieldKey: string) {
      const field = this.editableFields.find(f => f.key === fieldKey);
      if (field) {
        field.isEditing = !field.isEditing;
        if (field.isEditing) {
          this.editedReader[fieldKey] = this.reader[fieldKey];
        }
      }
    },
    //save edited field using put method
    async saveField(fieldKey: string) {
      try {
        const { cookies } = useCookies(); 
        const payload = { [fieldKey]: this.editedReader[fieldKey] };
        const response = await fetch(`http://localhost:8000/reader/${this.reader.id}/`, {
          method: "PUT",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Failed to update field");

        this.readerStore.saveReaders(await response.json());
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert(`Failed to update ${fieldKey}.`);
      }
    },
    //save edited goal using put
    async saveGoal(goalKey: string, value: number) {
      try {
        const { cookies } = useCookies();
        const payload = { [goalKey]: value };
        const response = await fetch(`http://localhost:8000/reader/${this.reader.id}/`, {
          method: "PUT",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Failed to update goal");

        this.readerStore.saveReaders(await response.json());
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert(`Failed to update ${goalKey}.`);
      }
    },
    //toggle goal to edit mode
    toggleGoalEdit(index: number) {
      const goal = this.goals[index];
      if (goal.isEditing) {
        this.saveGoal(goal.key, goal.value);
      }
      goal.isEditing = !goal.isEditing;
    },
    //accept friendship using put
    async acceptFriendship(friendshipId: number) {

      try {
        const { cookies } = useCookies();
        const response = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
          method: "PUT",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (!response.ok) throw new Error("Failed to accept friendship.");

        this.friendshipsStore.addFriendship(await response.json());
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert("Failed to accept friendship.");
      }
    },
    //delete friendship
    async deleteFriendship(friendshipId: number) {
      try {
        const { cookies } = useCookies();
        const response = await fetch(`http://localhost:8000/friendship/${friendshipId}/`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (!response.ok) throw new Error("Failed to delete friendship");

        this.friendshipsStore.removeFriendship(friendshipId);
        window.location.reload();
      } catch (error) {
        console.error("Error deleting friendship:", error);
        alert("Failed to delete friendship.");
      }
    },
  },
  setup() {
    return {
      readerStore: useReaderStore(),
      friendshipsStore: useFriendshipsStore(),
    };
  },
});
</script>


<style scoped>
/* General Styles */
.body {
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5em;  
  padding: 0.5em;  
  background-color: #EFE0CB;

}

/*style sections */
.top-section {
  display: flex;
  justify-content: space-between;
  gap: 0.5em; 
  width: 100%;
}

.bottom-section {
  display: flex;
  justify-content: space-between;
  gap: 0.5em; 
  width: 70%;

}

#profile-box,
#connections-box {
  background-color: #2f4a54;
  padding: 0.6em;  
  border-radius: 12px;
  width: 45%;
  min-width: 280px;  
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
  max-height: 350px; 
}

#connections-box {
  overflow-y: auto;
}

/*milestone  and goal sections*/
.milestone-message {
  color: #ffd700; 
  font-weight: bold;
  margin-top: 0.2em;  
  text-align: center;
}

.book-count-display , .goals-section {
  background-color: #2f4a54; 
  padding: 0.8em;  
  border-radius: 12px;
  width: 50%;
  max-width: 450px; 
  text-align: center;
  margin-top: 0.3em;  
  height: 150px;
}

.goals-section{
  overflow-y: auto;
}

.book-count-badge {
  background-color: #ffd700;
  padding: 0.4em 0.8em;  
  border-radius: 50px;
  color: #2f4a54;
  font-weight: bold;
  font-size: 1em;
  margin-bottom: 0.2em;
}

.book-count-progress {
  background-color: #ddd;
  height: 15px; 
  border-radius: 10px;
  width: 100%;
  margin: 0.3em 0;  
}

.progress-bar {
  height: 100%;
  background-color: #71929f;
  border-radius: 10px;
}

h2,
h3 {
  font-size: 1.4em;  
  color: #ffffff;
  text-align: center;
  margin-bottom: 0.6em;  
  font-weight: 600;
}

#profile-box p {
  color: #ffffff;
  background-color: #1e3640;
  padding: 0.4em;  
  border-radius: 8px;
  margin-bottom: 0.3em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#profile-box input {
  background-color: #f0f0f0;
  border: none;
  padding: 0.3em;
  border-radius: 5px;
  font-size: 1em;
}

.tabs {
  display: flex;
  justify-content: space-between;
  gap: 0.4em; 
  margin-bottom: 0.8em; 
}

.tab-group {
  display: flex;
  gap: 0.4em;
}

.connections-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8em;  
  max-height: 280px;  
  overflow-y: auto;
}

.connections-card {
  background-color: #1e3640;
  padding: 0.8em; 
  border-radius: 12px;
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.15);
  max-height: 230px;  
  overflow-y: auto;
}



ul {
  list-style: none;
  padding: 0;
}

li {
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.3em 0;  
  border-bottom: 1px solid #56707d;
}

li:last-child {
  border-bottom: none;
}

/*button styles */

button {
  background-color: #71929f;
  color: white;
  border: none;
  padding: 0.3em 0.6em;
  cursor: pointer;
  border-radius: 6px;
  font-size: 1em;
  transition: all 0.3s ease-in-out;
  
}

button:hover {
  background-color: #5a7c89;
  transform: scale(1.05);
}

.chosenButton {
  background-color: #ffffff;
  color: #2f4a54;
  font-weight: bold;
  border: 2px solid #71929f;
}

button:disabled {
  background-color: #d1d8e1;
  cursor: not-allowed;
}

button + button {
  margin-left: 6px;  
}

a {
    text-decoration: none;
    color: inherit;
}

/*responsive styles*/

@media (max-width: 768px) {
  .top-section, .bottom-section {
    flex-direction: column;
    align-items: center;
  }

  #profile-box,
  #connections-box {
    width: 90%;
  }

  .tabs {
    flex-direction: column;
    align-items: center;
  }

  .tab-group {
    flex-direction: column;
    align-items: center;
  }

  .connections-grid {
    grid-template-columns: 1fr;
  }

  .book-count-display {
    width: 80%;
  }
}
</style>
