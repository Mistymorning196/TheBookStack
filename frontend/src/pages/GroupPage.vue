<template>
  <ReaderNavBarComponent />
  <div class="body">
    <h1>Groups:</h1>

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
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useGroupsStore } from "../stores/groups";
import { Group } from "../types/index";

export default defineComponent({
  data() {
    return {
      query: "",  // The search query
      reader_id: null as number | null, // Initially null, will be populated after mounted
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
        const response = await fetch("https://thebookstack-2.onrender.com/groups/");
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

    // Fetch groups filtered by search query (by title or author)
    async fetchGroupsByQuery() {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/groups/?search=${this.query}`);
        const data = await response.json();
        const groups = data.groups as Group[];
        const storeGroup = useGroupsStore();
        storeGroup.saveGroups(groups);
      } catch (error) {
        console.error("Error fetching groups by query:", error);
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
  background-color: #efe0cb; /* Light background */
  min-height: 100vh;
  padding: 1rem;
  margin: 0;
  text-align: center;
}

/* Heading Styling */
h1 {
    color: white;
    background-color: #2f4a54; /* Dark background for headers */
    padding: 0.3rem 1rem; /* Reduced padding for better space usage */
    margin: 0.3rem 0; /* Reduced margin between titles */
    border-radius: 5px;
    font-size: 1.6rem; /* Reduced font size for smaller headings */
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
  max-height: 500px; /* Limit height for scrolling */
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

/* Responsive Design */
@media (max-width: 768px) {
  .scrollable-container {
    max-height: 400px; /* Adjust for mobile */
  }

  .group-card {
    width: 95%;
  }
}
</style>
