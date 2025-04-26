import { defineStore } from 'pinia'
import { Group } from '../types'

export const useGroupsStore = defineStore('groups', {
    state: () => ({ 
        groups: [] as Group[],
    }),
    actions: {
        saveGroups(groups: Group[]) {
            this.groups = groups
        },
        removeGroup(groupId: number) {
            this.groups = this.groups.filter((r) => r.id !== groupId);
        },
    }
})