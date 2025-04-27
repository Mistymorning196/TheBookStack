<template>
  <ReaderNavBarComponent />
  <div class="page-container">
    <!-- Group Title -->
    <h1 class="group-title" v-if="group">{{ group.name }}</h1>

    <!-- Discussion Box -->
    <section id="discussion-box" v-if="group">

      <!-- Scrollable Container -->
      <div class="discussions-container" ref="discussionContainer">
        <div
          v-for="(discussion, index) in discussions.filter(d => d.group === group?.id)"
          :key="index"
          class="discussion"
        >
          <p v-if="discussion.user === reader_id">
            <span>{{ discussion.username }}: {{ discussion.discussion }}</span>
            <button class="delete" @click="deleteDiscussion(discussion.id)">Delete</button>
          </p>
          <p v-else>{{ discussion.username }}: {{ discussion.discussion }}</p>
        </div>
      </div>
 
    </section>
    <button @click="toggleModal" class="add-button-container">Add Message</button>

    <!-- Add Discussion Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Add a Message</h3>
        <textarea v-model="newDiscussion.discussion" placeholder="Your message..."></textarea>
        <button @click="submitDiscussion">Submit</button>
        <button @click="toggleModal">Cancel</button>
      </div>
    </div>

    <div class="modal-overlay" v-if="showModal" @click="toggleModal"></div>
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useGroupStore } from "../stores/group";
import { useDiscussionsStore } from "../stores/discussions";
import { useRoute } from "vue-router";
import { useCookies } from "vue3-cookies";

interface NewDiscussion {
  discussion: string;
  group: number | null;
  user: number;
}

export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),
      showModal: false,
      newDiscussion: {
        discussion: "",
        group: null,
        user: Number(window.sessionStorage.getItem("reader_id")),
      } as NewDiscussion,
      group: undefined as { [x: string]: any; id: number; api: string; name: string; } | undefined,
    };
  },
  async mounted() {
    const route = useRoute();
    const groupId = parseInt(String(route.params.id)); 
    this.group = await this.groupStore.fetchGroupReturn(groupId);

    if (this.group) {
      let responseDiscussion = await fetch("https://thebookstack-2.onrender.com/discussions/");
      let dataDiscussion = await responseDiscussion.json();
      const storeDiscussion = useDiscussionsStore();
      storeDiscussion.saveDiscussions(dataDiscussion.discussions);

      this.newDiscussion.group = this.group.id; // Safe access
    }


    // Scroll to bottom after discussions are loaded
    this.scrollToBottom();
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    scrollToBottom() {
      // Wait for the DOM to update before scrolling
      this.$nextTick(() => {
        const container = this.$refs.discussionContainer as HTMLElement;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },

    toggleModal() {
      this.showModal = !this.showModal;
      const modalOverlay = document.querySelector('.modal-overlay');
      if (this.showModal) {
        if (modalOverlay) {
          modalOverlay.classList.add('active');
        }
      } else {
        if (modalOverlay) {
          modalOverlay.classList.remove('active');
        }
      }
    },

    async submitDiscussion() {
      if (!this.newDiscussion.discussion) {
        alert("Please fill out all fields!");
        return;
      }

      if (this.newDiscussion.group === null) {
        alert("Blog ID not set. Cannot submit comment.");
        return;
      }

      const { cookies } = useCookies();

      const discussionData = {
        id: 0,
        api: "",
        group_id: this.newDiscussion.group,
        user_id: this.reader_id,
        username: "Default Username",
        discussion: this.newDiscussion.discussion,
      };

      let response = await fetch("https://thebookstack-2.onrender.com/discussions/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${cookies.get("access_token")}`,
          "Content-Type": "application/json",
          "X-CSRFToken": cookies.get("csrftoken"),
        },
        credentials: "include",
        body: JSON.stringify(discussionData),
      });

      if (response.ok) {
        const storeDiscussion = useDiscussionsStore();
        storeDiscussion.saveDiscussions([...storeDiscussion.discussions, discussionData]);
        this.toggleModal();
        this.newDiscussion = {
          discussion: "",
          group: this.newDiscussion.group,
          user: this.reader_id,
        };
        
        window.location.reload();
        
      } else {
        alert("Failed to add discussion");
      }
    },

    async deleteDiscussion(discussionId: number) {
      try {
        const { cookies } = useCookies();
        const response = await fetch(`https://thebookstack-2.onrender.com/discussion/${discussionId}/`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken") 
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to delete discussion");
        }

        const discussionsStore = useDiscussionsStore();
        discussionsStore.removeDiscussion(discussionId);
        window.location.reload();
        alert("Discussion deleted successfully!");
      } catch (error) {
        console.error("Error deleting Discussion:", error);
        alert("Failed to delete Discussion. Please try again.");
      }
    },
  },
  computed: {
    discussions() {
      return this.storeDiscussion.discussions;
    },
  },
  setup() {
    const groupStore = useGroupStore();
    const storeDiscussion = useDiscussionsStore();
    return { groupStore, storeDiscussion };
  },
});
</script>

<style scoped>
/* Container for the entire page */
.page-container {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Group Title */
.group-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background-color: #542f2f;
  color: white;
  border-radius: 12px;
  box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.08);
}

/* Discussion Box Styling */
#discussion-box {
  width: 100%;
  max-width: 700px; /* Keep original max-width */
  background-color: #2f4a54;
  color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.25);
  display: block; /* Keep the original layout for discussions */
}

/* "Add Message" Button Styling */
#discussion-box button {
  background-color: #4b6c6f;
  color: white;
  padding: 10px 15px;
  margin-top: 1rem; /* Adjusted margin */
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: auto; /* This ensures the button's width is automatically adjusted to the content */
}

/* Center the "Add Message" button in its container */
.add-button-container {
  display: flex;
  justify-content: center;
  width: 100%; /* Ensure the container stretches fully to help with centering */
  margin-top: 1rem;
}

/* Discussions Container */
.discussions-container {
  max-height: 50vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  scroll-behavior: smooth;
  padding-right: 10px;
}

.discussion {
  background-color: #527a8a;
  padding: 3px 8px;
  border-radius: 8px;
}

.add-button-container{
  width: 400px;
}

.discussion button, .add-button-container {
  background-color: #4b6c6f;
  color: white;
  padding: 5px 10px;
  margin-left: 10px;
  margin-top: 2px;
  border-radius: 5px;
  cursor: pointer;
}

.discussion button:hover, .add-button-container:hover {
  background-color: #5d7f82;
  transform: translateY(-2px);
}

/* Modal Styling */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  width: 40%;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: -1;
}
</style>
