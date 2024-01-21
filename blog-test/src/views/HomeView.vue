<template>
  <div>
    <v-container>
      <v-row style="flex-direction: column; align-items: center">
        <v-col v-for="post in feed" :key="post.id" cols="12" md="4">
          <v-card class="mx-auto elevation-12" max-width="468">
            <v-img class="align-end" height="585" width="468" :src="post.midia" cover></v-img>
            <v-card-text style="font-size: 1rem">
              <div style="max-height: fit-content; min-height: 2rem">{{ post.description }}</div>
              <div>{{ post.locate }}</div>
              <div>Postado em {{ formatDate(post.date_post) }}</div>
              <div>{{ post.likes == 1 ? post.likes + ' curtida' : post.likes + ' curtidas' }}</div>
              <div style="margin-top: 0.8rem; color: #a8a8a8">
                Publicação de: <strong>{{ post.author }}</strong>
              </div>
            </v-card-text>
            <v-btn
              icon
              style="margin-left: 0.5rem; margin-bottom: 0.8rem"
              color="red-lighten-2"
              @click="like(post)"
            >
              <v-icon>mdi-heart-outline</v-icon>
            </v-btn>
            <v-btn
              icon
              disabled
              style="margin-left: 0.5rem; margin-bottom: 0.8rem"
              color="red-lighten-2"
            >
              <v-icon>mdi-share-variant-outline</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

interface Post {
  id: number
  description: string
  midia: string
  locate: string
  likes: number
  date_post: string
  author: string
}

export default defineComponent({
  data() {
    return {
      feed: [] as Post[]
    }
  },
  mounted() {
    this.fetchFeed()
  },
  methods: {
    async fetchFeed(): Promise<void> {
      try {
        const response = await axios.get('http://127.0.0.1:8000')
        this.feed = response.data.posts
      } catch (error: any) {
        console.error(error.message)
      }
    },
    formatDate(date: string): string {
      const formattedDate = new Date(date).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
      return formattedDate
    },
    async like(post: Post): Promise<void> {
      try {
        const updatedPost = await axios.put(`http://127.0.0.1:8000/like-post/${post.id}`)

        const index = this.feed.findIndex((p: any) => p.id === post.id)
        if (index !== -1) {
          this.feed[index] = updatedPost.data
        }
      } catch (error: any) {
        console.error(error.message)
      }
    }
  }
})
</script>
<style scoped></style>
