<template>
  <ReaderNavBarComponent />
  <div class="body">
    <h1>Groups:</h1>

    <!-- Button to open the modal for adding a new group -->
    <button @click="openGroupModal" class="btn btn-primary">Add New Group</button>

    <!-- Search bar input -->
    <input 
      v-model="query" 
      placeholder="Search by name..." 
      @input="search" 
      class="search-input" 
    />

    <!-- Scrollable section to show groups -->
    <section class="scrollable-container">
      <div v-for="(group, index) in filteredGroups" :key="index" class="group-card">
        <router-link :to="`/discussion/${group.id}`" class="group-link">
          <div class="group-title">
            <p> {{ group.name }}</p>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Modal to Add a New Group -->
    <div 
      v-if="showGroupModal"
      v-bind:class="['modal', { show: showGroupModal }]" 
      class="modal"
    >
      <div class="modal-content">
        <h4>Add New Group</h4>
        <form @submit.prevent="addGroup">
          <div class="form-group">
            <label for="groupName">Group Name</label>
            <input 
              type="text" 
              id="groupName" 
              v-model="newGroup.name" 
              required 
            />
          </div>
          <button type="submit" class="btn btn-success">Add Group</button>
          <button type="button" @click="closeGroupModal" class="btn btn-secondary">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useCookies } from "vue3-cookies";
import { useGroupsStore } from "../stores/groups";
import { Group } from "../types/index";

export default defineComponent({
  data() {
    return {
      query: "",  // The search query
      reader_id: null as number | null, // Initially null, will be populated after mounted
      showGroupModal: false,  // Flag to control modal visibility
      newGroup: { name: "" }, // New group data
    };
  },
  async mounted() {
    // Fetch all groups initially
    await this.fetchGroups();
  },
  computed: {
    // Filter groups based on the search query
    filteredGroups() {
      return this.groups.filter((group) => {
        const query = this.query.toLowerCase();
        return (
          group.name.toLowerCase().includes(query)
        );
      });
    },
    // Fetch groups from the store
    groups() {
      const storeGroup = useGroupsStore();
      return storeGroup.groups;
    },
  },
  methods: {
    // Fetch groups from the API and store them
    async fetchGroups() {
      try {
        const response = await fetch("http://localhost:8000/groups/");
        const data = await response.json();
        const groups = data.groups as Group[];
        const storeGroup = useGroupsStore();
        storeGroup.saveGroups(groups);
      } catch (error) {
        console.error("Error fetching groups:", error);
      }
    },

    // Search function called when user types in the search bar
    async search() {
      if (this.query.trim()) {
        await this.fetchGroupsByQuery();
      } else {
        await this.fetchGroups();  // Fetch all groups if the search query is empty
      }
    },

    // Fetch groups filtered by search query
    async fetchGroupsByQuery() {
      try {
        const response = await fetch(`http://localhost:8000/groups/?search=${this.query}`);
        const data = await response.json();
        const groups = data.groups as Group[];
        const storeGroup = useGroupsStore();
        storeGroup.saveGroups(groups);
      } catch (error) {
        console.error("Error fetching groups by query:", error);
      }
    },

    // Open the modal to add a new group
    openGroupModal() {
      this.showGroupModal = true;
    },

    // Close the modal
    closeGroupModal() {
      this.showGroupModal = false;
    },

    // Add the new group to the API
    async addGroup() {
      try {
        const { cookies } = useCookies();
        const response = await fetch("http://localhost:8000/groups/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify({
            name: this.newGroup.name,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to add group");
        }

        const data = await response.json();
        const storeGroup = useGroupsStore();
        storeGroup.saveGroups([...storeGroup.groups, data]); // Add the new group to the store
        this.closeGroupModal();  // Close the modal
        this.newGroup.name = "";  // Reset the new group input
      } catch (err) {
        console.error("Error adding group:", err);
        alert("Error adding group.");
      }
    },
  },
  components: {
    ReaderNavBarComponent,
  },
});
</script>

<style scoped>
/* General Styling */
.body {
  font-family: "Arial", sans-serif;
  background-color: #efe0cb; 
  min-height: 100vh;
  padding: 1rem;
  margin: 0;
  text-align: center;
}

/* Heading Styling */
h1 {
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

/* Search input styling */
.search-input {
  width: 100%;
  padding: 8px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 20px;
}

/* Scrollable Section */
.scrollable-container {
  max-height: 500px; 
  overflow-y: auto;
  background-color: #2f4a54;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Individual group Card */
.group-card {
  background-color: #71929f;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease-in-out;
  width: 90%;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.group-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
}

/* group Title */
.group-title {
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0;
  padding: 0.5rem;
  border-radius: 5px;
  background-color: #542f2f;
}

/* group Link */
.group-link {
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
}

.group-link:hover {
  color: #f0b400;
  transform: scale(1.05);
}

button {
  width: 100%;
  margin-top: 1rem;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #4b6c6f;
  color: white;
  border: none;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #5d7f82;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.3s ease;
  opacity: 0;
  visibility: hidden;
}

.modal-content {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  width: 300px;
}

.modal.show {
  opacity: 1;
  visibility: visible;
}

button[type="button"] {
  margin-top: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .scrollable-container {
    max-height: 400px; 
  }

  .group-card {
    width: 95%;
  }
}
</style>

