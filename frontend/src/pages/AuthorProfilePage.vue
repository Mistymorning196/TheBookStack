<template>
  <AuthorNavBarComponent />
  <div class="body">
    <div class="top-section">
      <!-- Profile Box -->
      <div id="profile-box">
        <h2>Welcome {{ author.first_name }}</h2>
        <p>Username: {{ author.username }} <button> <a href="http://localhost:8000/updateUser/"> Change Username </a> </button></p>

        <p v-for="field in editableFields" :key="field.key">
          <span v-if="!field.isEditing">{{ field.label }}: {{ author[field.key] }}</span>
          <span v-else>
            {{ field.label }}:
            <input v-model="editedAuthor[field.key]" :type="field.type" />
          </span>
          <button v-if="!field.isEditing" @click="toggleEditField(field.key)">Edit</button>
          <button v-else @click="saveField(field.key)">Save</button>
        </p>

        <button> <a href="http://localhost:8000/updatePass/"> Change Password </a> </button>
      </div>
       <!-- Biography Box -->
      <div id="bio-box">
        <h2>Author Biography:</h2>
        <p v-if="!isEditingBio">{{ author.biography }}</p>
        <textarea
          v-else
          v-model="editedBiography"
          :placeholder="author.biography || 'Enter your biography here...'"
        ></textarea>
        <button v-if="!isEditingBio" @click="toggleBioEdit">Edit</button>
        <button v-else @click="saveBiography">Save</button>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useAuthorStore } from "../stores/author";
import { useCookies } from "vue3-cookies";
import AuthorNavBarComponent from "../components/AuthorNav.vue";

export default defineComponent({
  data() {
    return {
      //for editing info
      editableFields: [
        { key: "first_name", label: "First Name", type: "text", isEditing: false },
        { key: "last_name", label: "Last Name", type: "text", isEditing: false },
        { key: "email", label: "Email", type: "email", isEditing: false },
        { key: "date_of_birth", label: "Date of Birth", type: "date", isEditing: false },
      ],
      editedAuthor: {} as Record<string, string>,
      author_id: Number(window.sessionStorage.getItem("reader_id")),
      isEditingBio: false,
      editedBiography: "",
    };
  },
  async mounted() {
    try {
      //fetch author
      const authorId = this.author_id;
      const author = await this.authorStore.fetchAuthorReturn(authorId);

      // Check if author is fetched properly
      if (author) {
        this.editedBiography = author.biography;
      } else {
        console.error("Author not found");
      }
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  },
  components: {
    AuthorNavBarComponent,
  },
  computed: {
    author() {
      return this.authorStore.author ?? {
        id: 0,
        api: '',
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        date_of_birth: 0,
        password: '',
        biography: '',
      };
    },
  },
  methods: {
    //switch fields to editable
    toggleEditField(fieldKey: string) {
      const field = this.editableFields.find(f => f.key === fieldKey);
      if (field) {
        field.isEditing = !field.isEditing;
        if (field.isEditing) {
          this.editedAuthor[fieldKey] = this.author[fieldKey];
        }
      }
    },
    //save edited fields using put method
    async saveField(fieldKey: string) {
      try {
        const { cookies } = useCookies();
        const payload = { [fieldKey]: this.editedAuthor[fieldKey] };
        const response = await fetch(`http://localhost:8000/author/${this.author.id}/`, {
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

        this.authorStore.saveAuthors(await response.json());
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert(`Failed to update ${fieldKey}.`);
      }
    },
    //make it so you can edit bio
    toggleBioEdit() {
      this.isEditingBio = !this.isEditingBio;
    },
    //save edited bio using put method
    async saveBiography() {
      try {
        const { cookies } = useCookies();
        const payload = { biography: this.editedBiography };
        const response = await fetch(`http://localhost:8000/author/${this.author.id}/`, {
          method: "PUT",
          headers: {
            "Authorization": `Bearer ${cookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": cookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Failed to update biography");

        this.authorStore.saveAuthors(await response.json());
        this.isEditingBio = false;
        window.location.reload();
      } catch (error) {
        console.error(error);
        alert("Failed to update biography.");
      }
    },
  },
  setup() {
    return {
      authorStore: useAuthorStore(),
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

.top-section {
  display: flex;
  justify-content: space-between;
  gap: 0.5em;  
  width: 100%;
}

#profile-box, #bio-box {
  background-color: #2f4a54;
  padding: 0.6em;  
  border-radius: 12px;
  width: 45%;
  min-width: 280px;  
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
  max-height: 350px;  
}

h2,
h3 {
  font-size: 1.4em; 
  color: #ffffff;
  text-align: center;
  margin-bottom: 0.6em;  
  font-weight: 600;
}

#profile-box p, #bio-box p {
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

/*media styles */
@media (max-width: 768px) {
  .top-section {
    flex-direction: column;
    align-items: center;
  }

  #profile-box {
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


  .book-count-display {
    width: 80%;
  }
}
</style>
