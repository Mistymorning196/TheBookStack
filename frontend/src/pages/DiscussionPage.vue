<template>
  <ReaderNavBarComponent />
  <div class="page-container">
    <!-- Group Title -->
    <h1 class="group-title">{{ group.name }}</h1>

    <!-- Discussion Box -->
    <section id="discussion-box">

      <!-- Scrollable Container -->
      <div class="discussions-container" ref="discussionContainer">
        <div
          v-for="(discussion, index) in discussions.filter(d => d.group === group.id)"
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
import { defineComponent, nextTick, onMounted, ref } from "vue";
import { useGroupStore } from "../stores/group";
import { useDiscussionsStore } from "../stores/discussions";
import { useRoute } from "vue-router";
import VueCookies from "vue-cookies";
import ReaderNavBarComponent from "../components/ReaderNav.vue";

export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),
      showModal: false,
      newDiscussion: {
        discussion: "",
        group: null,
        user: this.reader_id,
      },
    };
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
    },

    async submitDiscussion() {
      if (!this.newDiscussion.discussion) {
        alert("Please fill out all fields!");
        return;
      }

      const discussionData = {
        user_id: this.reader_id,
        group_id: this.newDiscussion.group,
        discussion: this.newDiscussion.discussion,
      };

      const response = await fetch("http://localhost:8000/discussions/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${VueCookies.get("access_token")}`,
          "Content-Type": "application/json",
          "X-CSRFToken": VueCookies.get("csrftoken"),
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
        await this.scrollToBottom();
      } else {
        alert("Failed to add discussion");
      }
    },

    async deleteDiscussion(discussionId: number) {
      try {
        const response = await fetch(`http://localhost:8000/discussion/${discussionId}/`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${VueCookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": VueCookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (!response.ok) throw new Error("Failed to delete");

        const discussionsStore = useDiscussionsStore();
        discussionsStore.removeDiscussion(discussionId);

        await this.scrollToBottom();
        alert("Message deleted successfully!");
      } catch (error) {
        alert("Failed to delete message.");
      }
    },
  },
  computed: {
    group() {
      return this.groupStore.group;
    },
    discussions() {
      return this.storeDiscussion.discussions;
    },
  },
  setup() {
    const groupStore = useGroupStore();
    const storeDiscussion = useDiscussionsStore();
    const discussionContainer = ref<HTMLElement | null>(null);

    const scrollToBottom = async () => {
      await nextTick();
      if (discussionContainer.value) {
        discussionContainer.value.scrollTop = discussionContainer.value.scrollHeight;
      }
    };

    onMounted(async () => {
      const route = useRoute();
      const groupId = parseInt(route.params.id);
      await groupStore.fetchGroupReturn(groupId);

      const response = await fetch("http://localhost:8000/discussions/");
      const data = await response.json();
      storeDiscussion.saveDiscussions(data.discussions);

      scrollToBottom();
    });

    return { groupStore, storeDiscussion, discussionContainer, scrollToBottom };
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
  border-radius: 8px;
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.modal-content button {
  margin: 0.5rem;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-container {
    padding: 1rem;
  }

  .group-title {
    font-size: 2rem;
  }

  #discussion-box {
    padding: 1rem;
  }
}

</style>
