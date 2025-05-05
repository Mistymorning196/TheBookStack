<template>
     <!-- Nav bar -->
  <AuthorNavBarComponent />
     <!-- form to make book-->
  <form @submit.prevent="submitBook" id="book-form" enctype="multipart/form-data">
    <h2>Upload a New Book</h2>

    <div class="form-group">
      <label for="bookTitle">Title</label>
      <input type="text" id="bookTitle" v-model="book.title" required />
    </div>

    <div class="form-group">
      <label for="bookAuthor">Author</label>
      <input type="text" id="bookAuthor" v-model="book.author" required />
    </div>

    <div class="form-group">
      <label for="bookBlurb">Blurb</label>
      <textarea id="bookBlurb" v-model="book.blurb" required />
    </div>

    <div class="form-group">
      <label for="bookISBN">ISBN</label>
      <input type="text" id="bookISBN" v-model="book.isbn" required />
    </div>

       <!-- upload cover image -->
    <div class="form-group">
      <label for="bookCover">Cover Image</label>
      <input type="file" id="bookCover" accept="image/*" @change="handleImageUpload" />
      <div v-if="previewUrl" class="preview-container">
        <p>Preview:</p>
        <img :src="previewUrl" alt="Cover preview" class="preview-img" />
      </div>
    </div>

       <!-- add genres -->
    <div class="form-group">
      <label for="bookGenre">Genre</label>
      <div v-if="genres.length" class="genres-container">
        <div v-for="genre in genres" :key="genre.id" class="genre-item">
          <input
            type="checkbox"
            :id="'genre-' + genre.id"
            :value="genre.id"
            v-model="selectedGenres"
          />
          <label :for="'genre-' + genre.id">{{ genre.type }}</label>
        </div>
      </div>
      <div v-else>
        <p>Loading genres...</p>
      </div>

      <!-- Button to open the Add Genre modal -->
      <button type="button" @click="openGenreModal" class="btn btn-secondary">Add New Genre</button>
    </div>

    <button type="submit">Submit Book</button>
  </form>

  <!-- Modal to Add a New Genre -->
  <div 
    v-if="showGenreModal"
    v-bind:class="['modal', { show: showGenreModal }]" 
    class="modal"
  >
    <div class="modal-content">
      <h4>Add New Genre</h4>
      <form @submit.prevent="addGenre">
        <div class="form-group">
          <label for="newGenre">Genre Name</label>
          <input type="text" id="newGenre" v-model="newGenre.type" required />
        </div>
        <div class="form-group">
          <label for="newDescription">Description</label>
          <input type="text" id="newDescription" v-model="newGenre.description" required />
        </div>
        <button type="submit" class="btn btn-success">Add Genre</button>
        <button type="button" @click="closeGenreModal" class="btn btn-secondary">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useCookies } from "vue3-cookies";
import AuthorNavBarComponent from "../components/AuthorNav.vue";
import { useGenresStore } from "../stores/genres";

export default defineComponent({
  components: {
    AuthorNavBarComponent,
  },
  setup() {
    //empty template
    const book = ref({
      title: "",
      author: "",
      blurb: "",
      isbn: "",
    });

    //store genres
    const selectedGenres = ref<number[]>([]);
    const genresStore = useGenresStore();
    const genres = ref(genresStore.genres);
    //open modal flag
    const showGenreModal = ref(false); 
    const newGenre = ref({
      type: "",
      description: ""
    });

    const author_id = Number(window.sessionStorage.getItem("reader_id"));

    //for cover image
    const coverFile = ref<File | null>(null);
    const previewUrl = ref<string | null>(null);

    const handleImageUpload = (event: Event) => {
      const target = event.target as HTMLInputElement;
      const file = target.files?.[0] || null;
      if (file) {
        coverFile.value = file;
        previewUrl.value = URL.createObjectURL(file);
      }
    };

    //method for submitting a book
    const submitBook = async () => {
      if (!book.value.title || !book.value.blurb || !book.value.isbn) {
        alert("Please fill out all fields!");
        return;
      }

      const formData = new FormData();
      formData.append("title", book.value.title);
      formData.append("author", book.value.author);
      formData.append("blurb", book.value.blurb);
      formData.append("isbn", book.value.isbn);
      if (coverFile.value) {
        formData.append("cover_image", coverFile.value);
      }

      try {
        const { cookies } = useCookies(); 
        const response = await fetch("http://localhost:8000/books/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${cookies.get("access_token")}`,
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: formData,
        });

        //if successfully made then make author book through
        if (!response.ok) throw new Error("Book creation failed");
        const createdBook = await response.json();

        await fetch("http://localhost:8000/author_books/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify({
            user_id: author_id,
            book_id: createdBook.id,
          }),
        });

        //makes book genre relationship for each of the selected genres
        for (const genreId of selectedGenres.value) {
          await fetch("http://localhost:8000/book_genres/", {
            method: "POST",
            headers: {
              Authorization: `Bearer ${cookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": cookies.get("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({
              book_id: createdBook.id,
              genre_id: genreId,
            }),
          });
        }

        // Reset
        book.value = { title: "", author: "", blurb: "", isbn: "" };
        selectedGenres.value = [];
        coverFile.value = null;
        previewUrl.value = null;
        window.location.href = "/authorHome";
      } catch (err) {
        console.error(err);
        alert("Error submitting book.");
      }
    };

    //fetch genres
    const fetchInitialData = async () => {
      try {
        const genreResponse = await fetch("http://localhost:8000/genres/");
        const data = await genreResponse.json();
        genresStore.saveGenres(data.genres ?? data);
        genres.value = genresStore.genres;
      } catch (err) {
        console.error("Failed to fetch genres", err);
      }

    };
    //modal methods
    const openGenreModal = () => {
      showGenreModal.value = true;
      console.log("openGenreModal called", showGenreModal.value);
    };

    const closeGenreModal = () => {
      showGenreModal.value = false;
      console.log("closeGenreModal called", showGenreModal.value);
    };

    //method to create a new modal
    const addGenre = async () => {
      try {
        const { cookies } = useCookies();
        const response = await fetch("http://localhost:8000/genres/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify({
            type: newGenre.value.type,
            description: newGenre.value.description,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to add genre");
        }

        const data = await response.json();
        genres.value.push(data); // Add the new genre to the list
        closeGenreModal();
        newGenre.value = { type: "", description: "" }; // Clear the input
      } catch (err) {
        console.error("Error adding genre:", err);
        alert("Error adding genre.");
      }
    };

    fetchInitialData();

    return {
      book,
      genres,
      selectedGenres,
      handleImageUpload,
      submitBook,
      previewUrl,
      showGenreModal,
      newGenre,
      openGenreModal,
      closeGenreModal,
      addGenre,
    };
  },
});
</script>

<style scoped>
/*styling for form */
#book-form {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #2f4a54;
  border-radius: 16px;
  box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.4);
  color: white;
}

h2 {
  text-align: center;
  background-color: #6a8b91;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 1.6rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 0.7rem;
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
  box-shadow: 0 0 0 2px rgba(106, 139, 145, 0.3);
}

textarea {
  min-height: 120px;
  resize: vertical;
}

/*styling for buttons*/
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

/*styling for genres*/
.genres-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}

.genre-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.genre-item label {
  font-weight: normal;
  color: #e0e0e0;
}

/*styling for image*/
.preview-container {
  margin-top: 1rem;
}

.preview-img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  margin-top: 0.5rem;
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
</style>

