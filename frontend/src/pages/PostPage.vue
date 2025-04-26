<template>
  <ReaderNavBarComponent />
  <div class="body">
    <!-- Post Section -->
    <div id="profile-box" v-if="blog">
      <h2>Post</h2>
      <p>Title: {{ blog.title }}</p>
      <p>Author: {{ blog.author }}</p>
      <p>Post: {{ blog.post }}</p>
    </div>


    <!-- Comment Section -->
    <section id="comment-box">
      <h2>Comments:</h2>
      <button @click="toggleModal">Add Comment</button>

      <!-- Scrollable Container for Comments -->
      <div class="comments-container">
        <div v-for="(comment, index) in comments.filter(comment => comment.blog === blog?.id)" :key="index" class="comment">
          <p v-if="comment.user === reader_id">
            <span>{{ comment.username }}: {{ comment.comment }}</span>
            <button class="delete" @click="deleteComment(comment.id)">Delete</button>
          </p>
          <p v-else>{{ comment.username }}: {{ comment.comment }}</p>
        </div>
      </div>
    </section>

    <!-- Add Comment Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Add a Comment</h3>
        <textarea v-model="newComment.comment" placeholder="Your comment..."></textarea>
        <button @click="submitComment">Submit</button>
        <button @click="toggleModal">Cancel</button>
      </div>
    </div>

    <!-- Modal Overlay (background) -->
    <div class="modal-overlay" v-if="showModal" @click="toggleModal"></div>
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent } from "vue";
import { useBlogStore } from "../stores/blog";
import { useCommentsStore } from "../stores/comments";
import { useRoute } from "vue-router";
import { useCookies } from "vue3-cookies";


interface NewComment {
  comment: string;
  blog: number | null;
  user: number;
}


export default defineComponent({
  data() {
    return {
      reader_id: Number(window.sessionStorage.getItem("reader_id")),

      // Modal and new comment
      showModal: false,
      
      newComment: {
        comment: "",
        blog: null,
        user: Number(window.sessionStorage.getItem("reader_id")),
      } as NewComment,


      blog: undefined as { [x: string]: any; id: number; api: string; title: string; post: string; author: string; } | undefined,
    };
  },
  async mounted() {
    const route = useRoute();
    const blogId = parseInt(String(route.params.id)); // Ensure blogId is a number
    this.blog = await this.blogStore.fetchBlogReturn(blogId);

    let responseComment = await fetch("http://localhost:8000/comments/");
    let dataComment = await responseComment.json();
    const storeComment = useCommentsStore();
    storeComment.saveComments(dataComment.comments);

    if (this.blog) {
      this.newComment.blog = this.blog.id; // Set blog ID for new comment
    }
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    // Toggle modal visibility
    toggleModal() {
      this.showModal = !this.showModal;
      const modalOverlay = document.querySelector('.modal-overlay');
      if (this.showModal) {
        if (modalOverlay) {
          modalOverlay.classList.add('active');
        } else {
          console.warn("Modal overlay not found");
        }
      } else {
        if (modalOverlay) {
          modalOverlay.classList.remove('active');
        }
      }
    },

    // Submit new comment
    async submitComment() {
      if (!this.newComment.comment) {
        alert("Please fill out all fields!");
        return;
      }

      if (this.newComment.blog === null) {
        alert("Blog ID not set. Cannot submit comment.");
        return;
      }

      const { cookies } = useCookies();

      // Create commentData that matches the Comment interface
      const commentData = {
        id: 0,  // Set to 0 or generate an actual ID if needed
        api: "", // Set an actual value if required for the API
        blog_id: this.newComment.blog,
        user_id: this.reader_id,
        username: "Default Username", // Use actual username from session or store
        comment: this.newComment.comment,
      };

      let response = await fetch("http://localhost:8000/comments/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${cookies.get("access_token")}`,
          "Content-Type": "application/json",
          "X-CSRFToken": cookies.get("csrftoken"),
        },
        credentials: "include",
        body: JSON.stringify(commentData),
      });

      if (response.ok) {
        const storeComment = useCommentsStore();
        storeComment.saveComments([...storeComment.comments, commentData]);
        this.toggleModal();
        this.newComment = {
          comment: "",
          blog: this.newComment.blog,
          user: this.reader_id,
        };
        window.location.reload();
      } else {
        alert("Failed to add comment");
      }
    },

    // Delete user's comment
    async deleteComment(commentId: number) {
      try {
        const { cookies } = useCookies();
        const response = await fetch(`http://localhost:8000/comment/${commentId}/`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to delete comment");
        }

        // Remove the deleted comment from the store
        const commentsStore = useCommentsStore();
        commentsStore.removeComment(commentId);

        window.location.reload();
        alert("Comment deleted successfully!");
      } catch (error) {
        console.error("Error deleting comment:", error);
        alert("Failed to delete comment. Please try again.");
      }
    },
  },
  computed: {
    comments() {
      const storeComment = useCommentsStore();
      return storeComment.comments;
    },
  },
  setup() {
    const blogStore = useBlogStore();
    const storeComment = useCommentsStore();
    return { blogStore, storeComment };
  },
});
</script>

  
  <style scoped>
  /* General Body Styling */
  .body {
    display: flex;
    justify-content: space-between;
    margin: 2rem;
  }
  
  /* Post Section */
  #profile-box {
    flex: 2; /* Make this section take more space */
    min-width: 400px;
    background-color: #2f4a54;
    color: white;
    padding: 1.5em;
    margin: 1em;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    transition: background-color 0.3s ease, transform 0.3s ease;
  }
  
  #profile-box:hover {
    background-color: #3a5f6f;
    transform: scale(1.05);
  }
  
  #profile-box h2 {
    text-align: center;
    background-color: #6a8b91;
    padding: 10px;
    border-radius: 5px;
    color: white;
    font-size: 1.5rem;
  }
  
  #profile-box p {
    font-size: 1rem;
    color: white;
    margin: 0.5em 0;
    background-color: #527a8a;
    padding: 0.2rem;
    border-radius: 8px;
    margin-bottom: 0.5em;
    box-shadow: 1px 1px 6px rgba(0, 0, 0, 0.1);
  }
  
  /* Comment Section */
  #comment-box {
    flex: 1; /* Smaller size for comments */
    min-width: 300px;
    background-color: #2f4a54;
    color: white;
    padding: 1.5em;
    margin: 1em;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    max-height: 75vh; /* Give some height for comments */
  }
  
  #comment-box button {
    background-color: #4b6c6f;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  #comment-box button:hover {
    background-color: #5d7f82;
  }
  
  /* Scrollable container for comments */
  .comments-container {
    max-height: 50vh;
    overflow-y: auto;
    padding-right: 10px;
  }
  
  /* Individual Comment Box */
  .comment {
    background-color: #527a8a;
    padding: 10px;
    margin: 5px 0;
    border-radius: 8px;
  }
  
  .comment button {
    background-color: #4b6c6f;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    margin-left: 10px;
  }
  
  .comment button:hover {
    background-color: #5d7f82;
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
  }
  
  .modal-content textarea {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  .modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3);
    visibility: hidden;
  }
  
  .modal-overlay.active {
    visibility: visible;
  }

  /* Media query for smaller screens */
@media (max-width: 768px) {


  .body{
    display: flex;
    flex-direction: column;
    align-items: center;
  }


}
  </style>
  
  