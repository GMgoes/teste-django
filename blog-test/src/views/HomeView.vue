<template>
  <div>
    <v-container>
      <v-row style="flex-direction: column; align-items: center">
        <v-col v-for="post in feed" :key="post.id" md="4">
          <v-card class="mx-auto elevation-12" style="background-color: #242323">
            <v-img class="align-end" height="585" :src="post.midia" cover></v-img>
            <v-card-text style="font-size: 1rem; color: floralwhite">
              <div style="max-height: fit-content; min-height: 2rem">{{ post.description }}</div>
              <div>{{ post.locate }}</div>
              <div>Postado em {{ formatDate(post.date_post) }}</div>
              <div>{{ post.likes == 1 ? post.likes + ' curtida' : post.likes + ' curtidas' }}</div>
              <div style="margin-top: 0.8rem; color: #a8a8a8">
                Publicação de: <strong>{{ post.author }}</strong>
              </div>
            </v-card-text>
            <v-btn style="margin-left: 0.5rem; margin-bottom: 0.8rem" @click="like(post)">
              <v-icon>mdi-heart-outline</v-icon>
            </v-btn>
            <v-btn disabled style="margin-left: 0.5rem; margin-bottom: 0.8rem">
              <v-icon>mdi-share-variant-outline</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
      <v-layout class="overflow-visible" style="height: 56px">
        <v-bottom-navigation :elevation="12" grow style="background-color: #212121">
          <v-btn value="recent" style="color: white">
            <v-icon>mdi-chat</v-icon>

            <span>Conversas</span>
          </v-btn>

          <v-btn value="favorites" style="color: white">
            <v-icon>mdi-heart</v-icon>

            <span>Notificações</span>
          </v-btn>

          <v-btn value="nearby" style="color: white">
            <v-icon>mdi-compass-outline</v-icon>

            <span>Explorar</span>
          </v-btn>
        </v-bottom-navigation>
      </v-layout>
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
  liked: boolean
}

export default defineComponent({
  data() {
    return {
      feed: [] as Post[],
      value: 1
    }
  },
  mounted() {
    this.fetchFeed()
  },
  methods: {
    async fetchFeed(): Promise<void> {
      try {
        const response = await axios.get('http://127.0.0.1:8000')
        this.feed = response.data.posts.map((post: Post) => ({
          ...post,
          liked: false
        }))
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
          this.feed[index].liked = true
          this.playClickSound()
        }
      } catch (error: any) {
        console.error(error.message)
      }
    },
    share() {},
    playClickSound() {
      const audio = new Audio('src/assets/audiocutter_facebook-like-sound-effect2.mp3')
      audio.play()
    }
  }
})
</script>
