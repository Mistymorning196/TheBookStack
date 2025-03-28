<template>
    <div class="body">
      <!-- Book Info Section -->
      <div id="profile-box">
        <h2>Book Info</h2>
        <p>Title: {{ book.title }}</p>
        <p>Author: {{ book.author }}</p>
        <p>Blurb: {{ book.blurb }}</p>
        <p>ISBN: {{ book.isbn }}</p>
        <p>Rating: {{ averageRating }} </p>
        <button v-if="statusBook === undefined" @click="addWishlist()">Add to WishList</button>
        <p v-else>Status: {{ statusBook }} </p>
      </div>
  
      <!-- Review Section -->
      <section id="review-box">
        <h2>Reviews</h2>
        <button @click="showModal = true">Add Review</button>
  
        <!-- Scrollable Container for Reviews -->
        <div class="reviews-container">
          <div v-for="(review, index) in reviews.filter(review => review.book === book.id)" :key="index">
            <p v-if="review.user === reader_id">
              <span v-if="!editTitle">Title: {{ review.title }}</span>
              <span v-else>
                Title:
                <input v-model="editedReview.title" type="text" />
              </span>
              <button v-if="!editTitle" @click="toggleEditField('Title')">Edit</button>
              <button v-else @click="saveField('title', review.id)">Save</button>
            </p>
            <p v-else>Title: {{ review.title }}</p>
  
            <p>Username: {{ review.username }}</p>
            <p v-if="review.user === reader_id">
              <span v-if="!editRating">Rating: {{ review.rating }} Stars</span>
              <span v-else>
                Rating:
                <select v-model="editedReview.rating">
                  <option v-for="n in 5" :key="n" :value="n">{{ n }} Stars</option>
                </select>
              </span>
              <button v-if="!editRating" @click="toggleEditField('Rating')">Edit</button>
              <button v-else @click="saveField('rating', review.id)">Save</button>
            </p>
            <p v-else>Rating: {{ review.rating }} Stars</p>
            <p v-if="review.user === reader_id">
              <span v-if="!editMessage">Message: {{ review.message }} </span>
              <span v-else>
                Message:
                <input v-model="editedReview.message" type="text" />
              </span>
              <button v-if="!editMessage" @click="toggleEditField('Message')">Edit</button>
              <button v-else @click="saveField('message', review.id)">Save</button>
            </p>
            <p v-else>Message: {{ review.message }} </p>
  
            <button v-if="review.user === reader_id" @click="deleteReview(review.id)">Delete</button>
          </div>
        </div>
      </section>
  
      <!-- Add Review Modal -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h3>Add a Review</h3>
          <input type="text" v-model="newReview.title" placeholder="Review Title" />
          <textarea v-model="newReview.message" placeholder="Your review..."></textarea>
          <label>Rating:</label>
          <select v-model="newReview.rating">
            <option v-for="n in 5" :key="n" :value="n">{{ n }} Stars</option>
          </select>
          <button @click="submitReview">Submit</button>
          <button @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { useBookStore } from "../stores/book";
  import { useReviewsStore } from "../stores/reviews";
  import { useRoute } from "vue-router";
  import VueCookies from "vue-cookies";
  import { UserBook } from "../types";
  import { useUserBooksStore } from "../stores/userBooks";
  
  export default defineComponent({
    data() {
      return {
        reader_id: Number(window.sessionStorage.getItem("reader_id")),
  
        // for making a new review
        showModal: false,
        newReview: {
          title: "",
          message: "",
          rating: 5,
          book: null,
          user: this.reader_id,
        },
  
        // for editing a review
        editTitle: false,
        editMessage: false,
        editRating: false,

  
        editedReview: {
          title: "",
          message: "",
          rating: "",
        },
      };
    },
    async mounted() {
      // gets the book information
      const route = useRoute();
      const bookId = parseInt(route.params.id);
      let book = await this.bookStore.fetchBookReturn(bookId);
  
      let responseReview = await fetch("http://localhost:8000/reviews/");
      let dataReview = await responseReview.json();
      const storeReview = useReviewsStore();
      storeReview.saveReviews(dataReview.reviews);
  
      this.newReview.book = bookId; // Set book ID for new review
  
      // get all the user book relationships
      let responseUserBook = await fetch("http://localhost:8000/user_books/");
      let dataUserBook = await responseUserBook.json();
      let userBooks = dataUserBook.user_books as UserBook[];
      const storeUserBook = useUserBooksStore();
      storeUserBook.saveUserBooks(userBooks);
    },
    methods: {
      // change the review to edit mode
      toggleEditField(field: string) {
        console.log(typeof field);
        this[`edit${field}`] = !this[`edit${field}`];
        if (this[`edit${field}`]) {
          this.editedReview[field.toLowerCase()] = this.review[field.toLowerCase()];
        }
      },
  
      async saveField(field: string, reviewID: number) {
        try {
          const payload = {
            [field.toLowerCase()]: this.editedReview[field.toLowerCase()],
          };
  
          const response = await fetch(`http://localhost:8000/review/${reviewID}/`, {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${VueCookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": VueCookies.get("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify(payload),
          });
  
          if (!response.ok) {
            throw new Error("Failed to update field");
          }
  
          const updatedReview = await response.json();
          console.log(updatedReview);
          //this.reviewStore = this.reviewStore.saveReviews(updatedReview); // Update the user state in the store
          console.log("Reloading...");
          window.location.reload(true);
  
          alert(`${field} updated successfully!`);
        } catch (error) {
          console.error(error);
          alert(`Failed to update ${field}.`);
        }
      },
  
      // creates new review for the book
      async submitReview() {
        if (!this.newReview.title || !this.newReview.message) {
          alert("Please fill out all fields!");
          return;
        }
  
        // Check if user already left a review for this book
        const existingReview = this.reviews.find(
          (review) => review.book === this.newReview.book && review.user === this.reader_id
        );
  
        if (existingReview) {
          alert("You have already reviewed this book!");
          return;
        }
  
        const reviewData = {
          user_id: this.reader_id,
          book_id: this.newReview.book,
          title: this.newReview.title,
          message: this.newReview.message,
          rating: this.newReview.rating,
        };
  
        let response = await fetch("http://localhost:8000/reviews/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${VueCookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": VueCookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify(reviewData),
        });
  
        if (response.ok) {
          const storeReview = useReviewsStore();
          storeReview.saveReviews([...storeReview.reviews, reviewData]);
          this.showModal = false;
          this.newReview = {
            title: "",
            message: "",
            rating: 5,
            book: this.newReview.book,
            user: this.reader_id,
          };
          window.location.reload();
          alert("Review added successfully");
        } else {
          alert("Failed to add review");
        }
      },
  
      // deletes the user's reviews
      async deleteReview(reviewId: number) {
        try {
          const response = await fetch(`http://localhost:8000/review/${reviewId}/`, {
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${VueCookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": VueCookies.get("csrftoken"),
            },
            credentials: "include",
          });
  
          if (!response.ok) {
            throw new Error("Failed to delete review");
          }
  
          // Remove the deleted friendship from the store
          const reviewsStore = useReviewsStore();
          reviewsStore.removeReview(reviewId);
  
          window.location.reload();
          alert("Review deleted successfully!");
        } catch (error) {
          console.error("Error deleting review:", error);
          alert("Failed to delete review. Please try again.");
        }
      },
  
      async addWishlist() {
        try {
          // Check if the book is already in userBooks
          const existingEntry = this.userBooks.find(
            (entry) => entry.user === this.reader_id && entry.book === this.book.id
          );
  
          if (existingEntry) {
            alert("This book is already in your list!");
            return;
          }
  
          // New userBook data
          const userBookData = {
            user_id: this.reader_id,
            book_id: this.book.id,
            status: "WISHLIST",
          };
  
          // Send POST request to backend
          let response = await fetch("http://localhost:8000/user_books/", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${VueCookies.get("access_token")}`,
              "Content-Type": "application/json",
              "X-CSRFToken": VueCookies.get("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify(userBookData),
          });
  
          if (!response.ok) {
            throw new Error("Failed to add book to wishlist.");
          }
  
          // Update store with the new userBook entry
          const newUserBook = await response.json();
          const storeUserBook = useUserBooksStore();
          storeUserBook.saveUserBooks([...storeUserBook.userBooks, newUserBook]);
  
          alert("Book added to wishlist!");
        } catch (error) {
          console.error(error);
          alert("Error adding book to wishlist.");
        }
      }
    },
    computed: {
      book() {
        return this.bookStore.book;
      },
      reviews() {
        const storeReview = useReviewsStore();
        return storeReview.reviews;
      },
      userBooks() {
        const storeUserBook = useUserBooksStore();
        return this.storeUserBook.userBooks;
      },
      statusBook() {
        const userBookEntry = this.userBooks.find(
          (entry) => entry.user === this.reader_id && entry.book === this.book.id
        );
        return userBookEntry ? userBookEntry.status : undefined;
      },
      averageRating() {
        const bookReviews = this.reviews.filter((review) => review.book === this.book.id);
        if (bookReviews.length === 0) return "No ratings yet";
  
        const total = bookReviews.reduce((sum, review) => sum + review.rating, 0);
        return (total / bookReviews.length).toFixed(1) + " Stars";
      }
    },
    setup() {
      const bookStore = useBookStore();
      const storeReview = useReviewsStore();
      const storeUserBook = useUserBooksStore();
      return { bookStore, storeReview, storeUserBook };
    }
  });
  </script>
  
<style scoped>
/* Book Info Section */
#profile-box {
  flex: 1;
  min-width: 300px;
  background-color: #2f4a54; /* Original background color */
  color: white; /* White text */
  padding: 1.5em; /* Reduced padding */
  margin: 1em;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s ease, transform 0.3s ease;
}

#profile-box:hover {
  background-color: #3a5f6f; /* Hover background */
  transform: scale(1.05);
}

#profile-box h2 {
  text-align: center;
  background-color: #6a8b91; /* Light grayish-blue background */
  padding: 10px;
  border-radius: 5px;
  color: white; /* White text for the title */
  font-size: 1.5rem;
}


/* Paragraph text inside #profile-box */
#profile-box p {
  font-size: 1rem;
  color: white; /* White text */
  margin: 0.5em 0;
  background-color: #527a8a;
  padding: 0.2rem;
  border-radius: 8px;
  margin-bottom: 0.5em;
  box-shadow: 1px 1px 6px rgba(0, 0, 0, 0.1);
}



/* Review Section */
#review-box {
  flex: 2;
  min-width: 400px;
  background-color: #2f4a54;
  padding: 1.5em; /* Reduced padding */
  margin: 1em;
  border-radius: 10px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s ease, transform 0.3s ease;
  max-height: 60vh; /* Set the max-height to be a percentage of the viewport */
  overflow: hidden; /* Hide overflow outside this container */
}

#review-box:hover {
  background-color: #3a5f6f;
  transform: scale(1.05);
}

#review-box h2 {
  text-align: center;
  background-color: #6a8b91;
  padding: 10px;
  border-radius: 5px;
  color: white;
  font-size: 1.5rem;
}

/* Scrollable container for reviews */
.reviews-container {
  max-height: calc(100% - 60px);  /* Adjust the height based on container's height */
  overflow-y: auto;   /* Enable vertical scrolling */
  padding-right: 15px; /* Ensure scrollbar doesn't overlap with content */
  box-sizing: border-box; /* Make sure padding is accounted for */
}

/* Review Cards */
#review-box > .reviews-container > div {
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
  transition: transform 0.2s ease-in-out;
}

#review-box > .reviews-container > div:nth-child(odd) {
  background-color: #3a5f6f;
}

#review-box > .reviews-container > div:nth-child(even) {
  background-color: #527a8a;
}

/* Hover Effect for Reviews */
#review-box > .reviews-container > div:hover {
  transform: scale(1.02);
  background-color: #638ea0;
}

/* Edit and Delete Buttons inside Reviews */
#review-box button {
  background-color: #4b6c6f;
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

#review-box button:hover {
  background-color: #5d7f82;
}

#review-box button:active {
  background-color: #4b6c6f;
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
  width: 350px; /* Reduced width */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-content input,
.modal-content textarea,
.modal-content select {
  width: 100%;
  padding: 10px;
  margin: 0.5rem 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.modal-content button {
  margin-top: 1rem;
  background-color: #4b6c6f;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #5d7f82;
}

.modal-content button:active {
  background-color: #4b6c6f;
}

/* General Body Styling */
.body {
  display: flex;
  justify-content: space-between;
  margin: 2rem;
}

/* Ensure the content in modal is vertically centered */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

input,
textarea,
select {
  font-size: 1rem;
}

h2 {
  font-size: 1.5rem;
}

button {
  cursor: pointer;
}

button:focus {
  outline: none;
}


</style>

  
  