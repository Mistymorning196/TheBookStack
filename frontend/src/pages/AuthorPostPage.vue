<template>
  <AuthorNavBarComponent />
    <div class="body">
      <!-- Post Section which author can edit-->
      <div id="profile-box">
        <h2>Post</h2>
        <p v-for="field in editableFields" :key="field.key">
          <span v-if="!field.isEditing">{{ field.label }}: {{ blog[field.key] }}</span>
          <span v-else>
            {{ field.label }}:
            <input v-model="editedBlog[field.key]" :type="field.type" />
          </span>
          <button v-if="!field.isEditing" @click="toggleEditField(field.key)">Edit</button>
          <button v-else @click="saveField(field.key)">Save</button>
        </p>
      </div>
  
      <!-- Comment Section -->
      <section id="comment-box">
        <h2>Comments:</h2>
  
        <!-- Scrollable Container for Comments -->
        <div class="comments-container">
          <div v-for="(comment, index) in comments.filter(comment => comment.blog === blog.id)" :key="index" class="comment">
            <p> {{comment.username}}: {{ comment.comment }}</p>
          </div>
        </div>
      </section>
  
    </div>
  </template>
  
  <script lang="ts">
  import AuthorNavBarComponent from "../components/AuthorNav.vue";
  import { defineComponent } from "vue";
  import { useBlogStore } from "../stores/blog";
  import { useCommentsStore } from "../stores/comments";
  import { useRoute } from "vue-router";
  import {useCookies} from "vue3-cookies";
  
  export default defineComponent({
    data() {
      return {
        reader_id: Number(window.sessionStorage.getItem("reader_id")), 
        editableFields: [
          { key: "title", label: "Title", type: "text", isEditing: false },
          { key: "author", label: "Author", type: "text", isEditing: false },
          { key: "post", label: "Post", type: "text", isEditing: false },
        ],
        editedBlog: {} as Record<string, string>,
      };
    },
    async mounted() {
      //fetch blogs
      const route = useRoute();
      const blogId = parseInt(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id); 

      await this.blogStore.fetchBlogReturn(blogId); 


      //fetch comments
      let responseComment = await fetch("http://localhost:8000/comments/");
      let dataComment = await responseComment.json();
      const storeComment = useCommentsStore();
      storeComment.saveComments(dataComment.comments);
  
    },
    components: {
      AuthorNavBarComponent,
    },
    methods: {
      //make fields editable
      toggleEditField(fieldKey: string) {
      const field = this.editableFields.find(f => f.key === fieldKey);
      if (field) {
        field.isEditing = !field.isEditing;
        if (field.isEditing) {
          this.editedBlog[fieldKey] = this.blog[fieldKey];
        }
      }
    },
    //save the changes using put method
    async saveField(fieldKey: string) {
      try {
        const { cookies } = useCookies(); 
        const payload = { [fieldKey]: this.editedBlog[fieldKey] };
        const response = await fetch(`http://localhost:8000/blog/${this.blog.id}/`, {
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

        this.blogStore.saveBlogs(await response.json());
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert(`Failed to update ${fieldKey}.`);
      }
    },
  
    },
    computed: {
      blog() {
        return this.blogStore.blog;
      },
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
    flex: 2;
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
    flex: 1; 
    min-width: 300px;
    background-color: #2f4a54;
    color: white;
    padding: 1.5em;
    margin: 1em;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    max-height: 75vh; 
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
  
  