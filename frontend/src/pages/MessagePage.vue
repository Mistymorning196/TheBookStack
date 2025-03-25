<template>
    <!-- Title Section -->
    <div class="title-container">
      <h1>Messages</h1>
    </div>
  
    <!-- Messages Container -->
    <div class="messages-container">
      <!-- Messages List (Scrollable) -->
      <div class="messages-list">
        <!-- Display messages between the current user and their friend -->
        <div v-for="message in filteredMessages" 
             :key="message.id" 
             :class="['message', message.user === reader_id ? 'outgoing' : 'incoming']">
          <p><strong>{{ message.userUsername }}:</strong> {{ message.message }}</p>
        </div>
      </div>
    </div>
  
    <!-- Form to send a new message -->
    <div class="message-form">
      <textarea v-model="newMessageText" placeholder="Write a message..." rows="2"></textarea>
      <button @click="sendMessage">Send</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, nextTick } from "vue";
  import { useMessagesStore } from "../stores/messages";
  import { useReaderStore } from "../stores/reader";
  import { useRoute } from "vue-router";
  import VueCookies from "vue-cookies";
  
  export default defineComponent({
    data() {
      return {
        reader_id: Number(window.sessionStorage.getItem("reader_id")),
        newMessageText: "", // New message input
      };
    },
    async mounted() {
      const route = useRoute();
      const readerId = parseInt(route.params.id);
      let reader = await this.readerStore.fetchReaderReturn(readerId);
  
      let responseMessage = await fetch("http://localhost:8000/messages/");
      let dataMessage = await responseMessage.json();
      let messages = dataMessage.messages;
      const storeMessages = useMessagesStore();
      storeMessages.saveMessages(messages);
  
      // Scroll to the bottom after messages are loaded
      this.scrollToBottom();
    },
    methods: {
      async sendMessage() {
        const newMessage = {
          user: this.reader_id,
          friend: this.reader.id,
          message: this.newMessageText,
        };
  
        const response = await fetch("http://localhost:8000/messages/", {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${VueCookies.get('access_token')}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': VueCookies.get('csrftoken'),
          },
          credentials: 'include',
          body: JSON.stringify(newMessage),
        });
  
        if (response.ok) {
          const savedMessage = await response.json();
          const storeMessages = useMessagesStore();
          storeMessages.addMessage(savedMessage.message);
  
          this.newMessageText = ""; // Clear message input
          window.location.reload();
          alert("Message sent!");
  
          // Scroll to the bottom after sending a message
          this.scrollToBottom();
        } else {
          alert("Error sending message.");
        }
      },
  
      // Scroll to the bottom of the messages list
      scrollToBottom() {
        nextTick(() => {
          const messagesList = document.querySelector('.messages-list');
          if (messagesList) {
            messagesList.scrollTop = messagesList.scrollHeight;
          }
        });
      },
    },
    computed: {
      reader() {
        return this.readerStore.reader;
      },
      messages() {
        return this.messagesStore.messages;
      },
      filteredMessages() {
        return this.messages.filter(
          (message) =>
            (message.user === this.reader.id && message.friend === this.reader_id) ||
            (message.friend === this.reader.id && message.user === this.reader_id)
        );
      },
    },
    setup() {
      const readerStore = useReaderStore();
      const messagesStore = useMessagesStore();
      return { readerStore, messagesStore };
    }
  });
  </script>
  
  <style scoped>
  /* Title Section */
  .title-container {
    background-color: #2f4a54;  /* Dark Blue background */
    text-align: center;
    padding: 0.5em; /* Further reduced padding */
    margin-bottom: 0.8em; /* Reduced margin */
    border-radius: 8px;
    width: 90%;  /* Same width as the message container */
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  
  /* Title Styling */
  .title-container h1 {
    font-size: 1.4rem;  /* Slightly smaller size */
    color: #e0f2f1;     /* Light color text */
    margin-bottom: 0;
    font-weight: bold;
    padding: 0.3em 0;
    border-bottom: 1px solid #5a7a87; /* Reduced border thickness */
    margin-top: 0;
  }
  
  /* Messages Container */
  .messages-container {
    background-color: #2f4a54;  /* Background color for message container */
    border: 2px solid #5a7a87; /* Border color */
    border-radius: 8px;
    padding: 0.8em; /* Reduced padding */
    margin: 0.4em auto; /* Reduced margin between containers */
    width: 90%;
    max-width: 600px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
  }
  
  /* Messages List (Scrollable) */
  .messages-list {
    max-height: 250px; /* Adjust height */
    overflow-y: auto;
    margin-bottom: 1em;
    padding-right: 10px;
  }
  
  /* Individual Message Styling */
  .message {
    padding: 0.5em;
    margin: 0.4em 0;
    border-radius: 8px;
    font-size: 0.9rem;  /* Reduced font size */
    word-wrap: break-word;
    border: 1px solid #5a7a87;
    box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  }
  
  /* Outgoing Messages (Current User) */
  .message.outgoing {
    background-color: #4d707d;
    color: white;
    align-self: flex-end;
    text-align: right;
    margin-left: auto;
  }
  
  /* Incoming Messages (Friend) */
  .message.incoming {
    background-color: #71929f;
    color: white;
    align-self: flex-start;
    text-align: left;
    margin-right: auto;
  }
  
  /* Message Sender Name */
  .message strong {
    display: block;
    font-size: 0.85rem;
    color: #e0f2f1;
  }
  
  /* Form Container (Centered) */
  .message-form {
    display: flex;
    flex-direction: column;
    gap: 0.5em; /* Reduced gap */
    margin-top: 0.6em; /* Reduced margin between message container and form */
    padding: 0.8em; /* Reduced padding */
    background-color: #3a545d;  /* Matching message container background */
    border-radius: 8px;
    box-shadow: 1px 1px 6px rgba(0, 0, 0, 0.2);
    border: 2px solid #5a7a87;  /* Matching border */
    width: 90%;  /* Same width as message container */
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  
  /* Message Input Area */
  .message-form textarea {
    width: 100%;
    padding: 0.5em;  /* Reduced padding */
    border-radius: 6px;
    border: 1px solid #4d707d;
    background-color: #2f4a54;  /* Matching background */
    color: white;
    font-size: 0.9rem;
    resize: none;
    box-shadow: inset 0 0 3px rgba(0, 0, 0, 0.2);
  }
  
  /* Send Button */
  .message-form button {
    background-color: #4d707d;
    font-size: 1rem;
    padding: 0.4em 1em;  /* Reduced padding */
    border: none;
    color: white;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    transition: transform 0.2s ease, background 0.3s ease-in-out;
    align-self: center;
    width: 50%;
    box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  }
  
  .message-form button:hover {
    background-color: #5e8a97;
    transform: scale(1.05);
  }
  </style>
  
  