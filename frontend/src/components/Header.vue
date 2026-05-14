     1|<template>
     2|  <header class="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
     3|    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
     4|      <div class="flex justify-between items-center h-16">
     5|        <!-- Logo -->
     6|        <div class="flex items-center">
     7|          <router-link to="/" class="flex items-center space-x-2">
     8|            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-500 rounded-lg flex items-center justify-center">
     9|              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    10|                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
    11|              </svg>
    12|            </div>
    13|            <span class="text-lg font-bold text-gray-900">地理旅游知识问答</span>
    14|          </router-link>
    15|        </div>
    16|
    17|        <!-- Navigation -->
    18|        <nav class="hidden md:flex items-center space-x-1">
    19|          <router-link
    20|            v-for="item in navItems"
    21|            :key="item.path"
    22|            :to="item.path"
    23|            class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
    24|            :class="isActive(item.path) ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
    25|          >
    26|            {{ item.name }}
    27|          </router-link>
    28|        </nav>
    29|
    30|        <!-- User Menu -->
    31|        <div class="flex items-center space-x-4">
    32|          <div v-if="authStore.isLoggedIn" class="flex items-center space-x-3">
    33|            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
    34|              <span class="text-sm font-medium text-primary-700">
    35|                {{ authStore.user?.username?.charAt(0).toUpperCase() }}
    36|              </span>
    37|            </div>
    38|            <span class="text-sm text-gray-700 hidden sm:block">{{ authStore.user?.username }}</span>
    39|            <button
    40|              @click="handleLogout"
    41|              class="text-sm text-gray-500 hover:text-red-500 transition-colors"
    42|            >
    43|              退出
    44|            </button>
    45|          </div>
    46|        </div>
    47|      </div>
    48|    </div>
    49|
    50|    <!-- Mobile Navigation -->
    51|    <div class="md:hidden border-t border-gray-100">
    52|      <div class="flex">
    53|        <router-link
    54|          v-for="item in navItems"
    55|          :key="item.path"
    56|          :to="item.path"
    57|          class="flex-1 py-3 text-center text-sm font-medium transition-colors"
    58|          :class="isActive(item.path) ? 'text-primary-700 border-b-2 border-primary-500' : 'text-gray-500'"
    59|        >
    60|          {{ item.name }}
    61|        </router-link>
    62|      </div>
    63|    </div>
    64|  </header>
    65|</template>
    66|
    67|<script setup lang="ts">
    68|import { useRouter, useRoute } from 'vue-router'
    69|import { useAuthStore } from '@/stores/auth'
    70|
    71|const router = useRouter()
    72|const route = useRoute()
    73|const authStore = useAuthStore()
    74|
    75|const navItems = [
    76|  { name: '知识问答', path: '/' },
    77|  { name: '知识图谱', path: '/knowledge' }
    78|]
    79|
    80|function isActive(path: string) {
    81|  return route.path === path
    82|}
    83|
    84|function handleLogout() {
    85|  authStore.logout()
    86|  router.push('/login')
    87|}
    88|</script>
    89|