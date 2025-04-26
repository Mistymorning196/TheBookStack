import { defineStore } from "pinia";
import { Group } from "../types";

export const useGroupStore = defineStore("group", {
  state: (): {group: Group} => ({
    
    group: {} as Group, // Holds the currently selected group
  }),

  actions: {
    // Save the list of groups
    saveGroups(group: Group) {
      this.group = group;
    },


    // Fetch a single group by ID from the backend
    async fetchGroup(groupId: number) {
      try {
        const response = await fetch(`http://localhost:8000/group/${groupId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch group data");
        }
        const groupData = await response.json();
        this.group = groupData; // Update the state with the fetched group data
      
      } catch (error) {
        console.error("Error fetching group data:", error);
      }
    },

    async fetchGroupReturn(groupId: number) {
      try {
        const response = await fetch(`http://localhost:8000/group/${groupId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch group data");
        }
        const groupData = await response.json();
        this.group = groupData; // Update the state with the fetched group data
        return this.group
      } catch (error) {
        console.error("Error fetching group data:", error);
      }
    },
  },
});