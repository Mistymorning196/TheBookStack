<template>
  <AuthorNavBarComponent />
  <form @submit.prevent="submitBlog" id="blog-form">
    <h2>Write a New Blog</h2>
    <div class="form-group">
      <label for="blogTitle">Title</label>
      <input type="text" id="blogTitle" v-model="blog.title" required />
    </div>

    <div class="form-group">
      <label for="blogPost">Post</label>
      <textarea id="blogPost" v-model="blog.post" required />
    </div>

    <button type="submit">Submit Blog</button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import VueCookies from "vue-cookies";
import AuthorNavBarComponent from "../components/AuthorNav.vue";

export default defineComponent({
  components: {
    AuthorNavBarComponent,
  },
  data() {
    return {
      author_id: Number(window.sessionStorage.getItem("reader_id")),
      blog: {
        title: "",
        post: "",
        author: "",
      },
    };
  },
  async mounted() {
    // Fetch author info
    try {
      const response = await fetch(`http://localhost:8000/author/${this.author_id}`, {
        headers: {
          Authorization: `Bearer ${VueCookies.get("access_token")}`,
        },
        credentials: "include",
      });
      if (!response.ok) throw new Error("Failed to fetch author");
      const data = await response.json();
      this.blog.author = `${data.first_name} ${data.last_name}`;
    } catch (err) {
      console.error("Failed to fetch author info", err);
      this.blog.author = "Unknown Author";
    }
  },
  methods: {
    async submitBlog() {
      if (!this.blog.title || !this.blog.post) {
        alert("Please fill out all fields!");
        return;
      }

      try {
        const blogResponse = await fetch("http://localhost:8000/blogs/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${VueCookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": VueCookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify(this.blog),
        });

        if (!blogResponse.ok) throw new Error("Failed to create blog");

        const createdBlog = await blogResponse.json();

        const authorBlogResponse = await fetch("http://localhost:8000/author_blogs/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${VueCookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": VueCookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify({
            user_id: this.author_id,
            blog_id: createdBlog.id,
          }),
        });

        if (!authorBlogResponse.ok) throw new Error("Failed to link blog to author");

        this.blog = { title: "", post: "" };
        this.$router.push("/authorHome");
      } catch (error) {
        console.error(error);
        alert("There was an error posting your blog.");
      }
    },
  },
});
</script>

<style scoped>
#blog-form {
  max-width: 350px;
  margin: 0.5rem auto;
  padding: 1rem;
  background-color: #2f4a54;
  border-radius: 16px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
  color: white;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

#blog-form h2 {
  text-align: center;
  background-color: #6a8b91;
  padding: 10px;
  border-radius: 8px;
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #527a8a;
  color: white;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #6a8b91;
  box-shadow: 0 0 0 3px rgba(106, 139, 145, 0.3);
}

textarea {
  min-height: 150px;
  resize: vertical;
}

button {
  width: 100%;
  margin-top: 1.5rem;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #4b6c6f;
  color: white;
  border: none;
  border-radius: 8px;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

button:hover {
  background-color: #5d7f82;
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}
</style>

