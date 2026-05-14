     1|<template>
     2|  <div class="flex flex-col h-screen bg-gray-50">
     3|    <Header />
     4|    
     5|    <div class="flex-1 overflow-hidden flex flex-col">
     6|      <!-- Welcome Section (when no messages) -->
     7|      <div v-if="messages.length === 0" class="flex-1 flex items-center justify-center p-4">
     8|        <div class="text-center max-w-2xl">
     9|          <div class="w-20 h-20 bg-gradient-to-br from-primary-500 to-purple-500 rounded-3xl flex items-center justify-center mx-auto mb-6">
    10|            <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    11|              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    12|            </svg>
    13|          </div>
    14|          <h2 class="text-3xl font-bold text-gray-900 mb-3">地理旅游知识问答</h2>
    15|          <p class="text-gray-500 mb-8 text-lg">基于知识图谱的智能问答，输入任何问题开始探索</p>
    16|          
    17|          <!-- Recommended Questions -->
    18|          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl mx-auto">
    19|            <button
    20|              v-for="q in recommendedQuestions"
    21|              :key="q"
    22|              @click="sendMessage(q)"
    23|              class="p-4 bg-white rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all text-left text-sm text-gray-700 hover:text-primary-600"
    24|            >
    25|              <svg class="w-4 h-4 text-primary-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    26|                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
    27|              </svg>
    28|              {{ q }}
    29|            </button>
    30|          </div>
    31|        </div>
    32|      </div>
    33|
    34|      <!-- Chat Messages -->
    35|      <div v-else ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
    36|        <div
    37|          v-for="(msg, idx) in messages"
    38|          :key="idx"
    39|          class="flex"
    40|          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
    41|        >
    42|          <!-- Assistant Avatar -->
    43|          <div v-if="msg.role === 'assistant'" class="flex-shrink-0 mr-3">
    44|            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-500 rounded-full flex items-center justify-center">
    45|              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    46|                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
    47|              </svg>
    48|            </div>
    49|          </div>
    50|
    51|          <!-- Message Bubble -->
    52|          <div
    53|            class="max-w-[70%] px-4 py-3"
    54|            :class="msg.role === 'user' ? 'bubble-user' : 'bubble-assistant'"
    55|          >
    56|            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
    57|            
    58|            <!-- Entities -->
    59|            <div v-if="msg.entities && msg.entities.length > 0" class="mt-3 pt-3 border-t border-gray-200/50">
    60|              <div class="text-xs text-gray-500 mb-1">识别到的实体：</div>
    61|              <div class="flex flex-wrap gap-1">
    62|                <span v-for="entity in msg.entities" :key="entity" class="entity-tag">
    63|                  {{ entity }}
    64|                </span>
    65|              </div>
    66|            </div>
    67|          </div>
    68|
    69|          <!-- User Avatar -->
    70|          <div v-if="msg.role === 'user'" class="flex-shrink-0 ml-3">
    71|            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
    72|              <span class="text-sm font-medium text-primary-700">
    73|                {{ authStore.user?.username?.charAt(0).toUpperCase() }}
    74|              </span>
    75|            </div>
    76|          </div>
    77|        </div>
    78|
    79|        <!-- Loading Indicator -->
    80|        <div v-if="loading" class="flex justify-start">
    81|          <div class="flex-shrink-0 mr-3">
    82|            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-500 rounded-full flex items-center justify-center">
    83|              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    84|                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
    85|              </svg>
    86|            </div>
    87|          </div>
    88|          <div class="bubble-assistant px-4 py-3">
    89|            <div class="flex space-x-2">
    90|              <div class="w-2 h-2 bg-gray-400 rounded-full bounce-dot" />
    91|              <div class="w-2 h-2 bg-gray-400 rounded-full bounce-dot" />
    92|              <div class="w-2 h-2 bg-gray-400 rounded-full bounce-dot" />
    93|            </div>
    94|          </div>
    95|        </div>
    96|      </div>
    97|
    98|      <!-- Input Area -->
    99|      <div class="border-t border-gray-200 bg-white p-4">
   100|        <form @submit.prevent="sendMessage(inputText)" class="flex space-x-3 max-w-4xl mx-auto">
   101|          <input
   102|            v-model="inputText"
   103|            type="text"
   104|            placeholder="输入您的问题..."
   105|            :disabled="loading"
   106|            class="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
   107|          />
   108|          <button
   109|            type="submit"
   110|            :disabled="!inputText.trim() || loading"
   111|            class="btn-primary text-white px-6 py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
   112|          >
   113|            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
   114|              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
   115|            </svg>
   116|          </button>
   117|        </form>
   118|      </div>
   119|    </div>
   120|  </div>
   121|</template>
   122|
   123|<script setup lang="ts">
   124|import { ref, nextTick, onMounted } from 'vue'
   125|import { useAuthStore } from '@/stores/auth'
   126|import { qaApi } from '@/api/qa'
   127|import type { ChatMessage } from '@/types'
   128|import Header from '@/components/Header.vue'
   129|
   130|const authStore = useAuthStore()
   131|const messages = ref<ChatMessage[]>([])
   132|const inputText = ref('')
   133|const loading = ref(false)
   134|const chatContainer = ref<HTMLElement>()
   135|
   136|const recommendedQuestions = [
   137|  '红色食品是什么？',
   138|  '大龙湫在哪里？',
   139|  '什么是人工智能？',
   140|  '太阳系有哪些行星？'
   141|]
   142|
   143|async function sendMessage(text: string) {
   144|  if (!text.trim() || loading.value) return
   145|  
   146|  const question = text.trim()
   147|  inputText.value = ''
   148|  
   149|  // Add user message
   150|  messages.value.push({
   151|    role: 'user',
   152|    content: question,
   153|    timestamp: Date.now()
   154|  })
   155|  
   156|  // Scroll to bottom
   157|  await nextTick()
   158|  scrollToBottom()
   159|  
   160|  // Send to API
   161|  loading.value = true
   162|  try {
   163|    const result = await qaApi.ask({ question })
   164|    messages.value.push({
   165|      role: 'assistant',
   166|      content: result.answer,
   167|      entities: result.entities,
   168|      timestamp: Date.now()
   169|    })
   170|  } catch (e: any) {
   171|    messages.value.push({
   172|      role: 'assistant',
   173|      content: '抱歉，处理您的问题时出现了错误，请稍后重试。',
   174|      timestamp: Date.now()
   175|    })
   176|  } finally {
   177|    loading.value = false
   178|    await nextTick()
   179|    scrollToBottom()
   180|  }
   181|}
   182|
   183|function scrollToBottom() {
   184|  if (chatContainer.value) {
   185|    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
   186|  }
   187|}
   188|
   189|onMounted(() => {
   190|  // Focus input on mount
   191|  const input = document.querySelector('input[type="text"]') as HTMLInputElement
   192|  input?.focus()
   193|})
   194|</script>
   195|