<template>
    <div class="body">
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

      <section id="review-box">
          <h2>Reviews</h2>
          <button @click="showModal = true">Add Review</button>
          
          <div v-for="(review, index) in reviews.filter(review => review.book === book.id)" :key="index">
            <p v-if="review.user === user_id">
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
            <p v-if="review.user === user_id">
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
            <p v-if="review.user === user_id">
                <span v-if="!editMessage">Message: {{ review.message }} </span>
                    <span v-else>
                        Message:
                        <input v-model="editedReview.message" type="text" />
                    </span>
                    <button v-if="!editMessage" @click="toggleEditField('Message')">Edit</button>
                    <button v-else @click="saveField('message', review.id)">Save</button>
            </p>
            <p v-else>Message: {{ review.message }} </p> 
            
            <button v-if="review.user === user_id" @click="deleteReview(review.id)">Delete</button>
          </div>       
      </section>

      <!-- Add Review Modal -->
      <div v-if="showModal" class="modal">
          <div class="modal-content">
              <h3>Add a Review</h3>
              <input type="text" v-model="newReview.title" placeholder="Review Title">
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
            user_id: Number(window.sessionStorage.getItem("user_id")),

            //for making a new review
            showModal: false,
            newReview: {
                title: "",
                message: "",
                rating: 5,
                book: null,
                user: this.user_id
            },

            //for editing a review
            editTitle: false,
            editMessage: false,
            editRating: false,
            activeTab: "accepted", // Default to Accepted Friends

            editedReview: {
                title: "",
                message: "",
                rating: "",                
            },
        };
    },
    async mounted() {
        //gets the book information 
        const route = useRoute();
        const bookId = parseInt(route.params.id);
        let book = await this.bookStore.fetchBookReturn(bookId);

        let responseReview = await fetch("http://localhost:8000/reviews/");
        let dataReview = await responseReview.json();
        const storeReview = useReviewsStore();
        storeReview.saveReviews(dataReview.reviews);

        this.newReview.book = bookId; // Set book ID for new review

        //get all the user book relationships
        let responseUserBook = await fetch("http://localhost:8000/user_books/");
        let dataUserBook = await responseUserBook.json();
        let userBooks = dataUserBook.user_books as UserBook[];
        const storeUserBook = useUserBooksStore()
        storeUserBook.saveUserBooks(userBooks) 
    },
    methods: {
        //change the review to edit mode
        toggleEditField(field: string) {
            console.log(typeof field)
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
                        'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': VueCookies.get('csrftoken'),
                    },
                    credentials: 'include',
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    throw new Error("Failed to update field");
                }

                const updatedReview = await response.json();
                console.log(updatedReview)
                //this.reviewStore = this.reviewStore.saveReviews(updatedReview); // Update the user state in the store
                console.log("Reloading...");
                window.location.reload(true);
            
                alert(`${field} updated successfully!`);
            } catch (error) {
                console.error(error);
                alert(`Failed to update ${field}.`);
            }
        },
        
        //creates new review for the book
        async submitReview() {
            if (!this.newReview.title || !this.newReview.message) {
                alert("Please fill out all fields!");
                return;
            }

             // Check if user already left a review for this book
            const existingReview = this.reviews.find(
                (review) => review.book === this.newReview.book && review.user === this.user_id
            );

            if (existingReview) {
                alert("You have already reviewed this book!");
                return;
            }

            const reviewData = {
                user_id: this.user_id,
                book_id: this.newReview.book,
                title: this.newReview.title,
                message: this.newReview.message,
                rating: this.newReview.rating
            };

            let response = await fetch("http://localhost:8000/reviews/", {
                method: "POST",
                headers: {
                    'Authorization': `Bearer ${VueCookies.get('access_token')}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': VueCookies.get('csrftoken'),
                },
                credentials: "include",
                body: JSON.stringify(reviewData)
            });

            if (response.ok) {
                const storeReview = useReviewsStore();
                storeReview.saveReviews([...storeReview.reviews, reviewData]);
                this.showModal = false;
                this.newReview = { title: "", message: "", rating: 5, book: this.newReview.book, user: this.user_id };
                window.location.reload();
                alert("Review added successfully")
            } else {
                alert("Failed to add review");
            }
        },
        //deletes the users reviews
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

              //Remove the deleted friendship from the store
              const reviewsStore = useReviewsStore();
              reviewsStore.removeReview(reviewId);

              window.location.reload();
              alert("Review deleted successfully!");
            } catch (error) {
              console.error("Error deleting review:", error);
              alert("Failed to delete review. Please try again.");
            }
          },

        async addWishlist(){
            try {
                // Check if the book is already in userBooks
                const existingEntry = this.userBooks.find(
                    (entry) => entry.user === this.user_id && entry.book === this.book.id
                );

                if (existingEntry) {
                    alert("This book is already in your list!");
                    return;
                }

                // New userBook data
                const userBookData = {
                    user_id: this.user_id,
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
        userBooks(){
            const storeUserBook = useUserBooksStore();
            return this.storeUserBook.userBooks;
        },
        statusBook() {
            const userBookEntry = this.userBooks.find(
                (entry) => entry.user === this.user_id && entry.book === this.book.id
            );
            return userBookEntry ? userBookEntry.status : undefined;
        },
        averageRating() {
            const bookReviews = this.reviews.filter(review => review.book === this.book.id);
            if (bookReviews.length === 0) return "No ratings yet";

            const total = bookReviews.reduce((sum, review) => sum + review.rating, 0);
            return (total / bookReviews.length).toFixed(1) + " Stars";
        }
    },
    setup() {
        const bookStore = useBookStore();
        const storeReview = useReviewsStore();
        const storeUserBook = useUserBooksStore();
        return { bookStore, storeReview, storeUserBook};
    }
});
</script>
  
  <style scoped>
    .body{
        font-family: Arial, Helvetica, sans-serif;
        display: flex;
    }

    .body > div, #review-box{
        background-color: #2f4a54;
        margin:2em;
        padding:2em;
    }

  
    a{
        background-color: #2f4a54;
        margin:0.5em;
        text-decoration: none;
        color:black;
        padding: 0.2em;
    }
  
    a:hover, button:hover{
        color:grey;
    }
  
    h2, div>p, section>div {
        background-color: #71929f;
        margin:0.2em;
        color: white;
    }
    h6{
        text-align: center;
    }

    li{
        color: white;
        style:none;
    }

    li>button{
        background-color: #71929f;
        margin-left: 0.5em;
    }
  
    button{
        background-color:  #2f4a54;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        border: none;
        color: white;
        border-style:ridge;
    }

    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }

    .modal-content input, .modal-content textarea, .modal-content select {
        width: 100%;
        margin: 10px 0;
        padding: 8px;
    }

    .modal-content button {
        margin: 10px;
        padding: 10px;
        cursor: pointer;
    }
  
  </style>
  
  