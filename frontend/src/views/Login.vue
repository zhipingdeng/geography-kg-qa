     1|<template>
     2|  <div class="min-h-screen gradient-bg flex items-center justify-center p-4">
     3|    <div class="w-full max-w-md">
     4|      <!-- Card -->
     5|      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
     6|        <!-- Header -->
     7|        <div class="p-8 pb-6 text-center">
     8|          <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
     9|            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    10|              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
    11|            </svg>
    12|          </div>
    13|          <h1 class="text-2xl font-bold text-gray-900">地理旅游知识问答</h1>
    14|          <p class="text-gray-500 mt-2">基于知识图谱的智能问答系统</p>
    15|        </div>
    16|
    17|        <!-- Tabs -->
    18|        <div class="flex border-b border-gray-100">
    19|          <button
    20|            v-for="tab in tabs"
    21|            :key="tab.key"
    22|            @click="activeTab = tab.key"
    23|            class="flex-1 py-3 text-sm font-medium transition-colors relative"
    24|            :class="activeTab === tab.key ? 'text-primary-600' : 'text-gray-500 hover:text-gray-700'"
    25|          >
    26|            {{ tab.label }}
    27|            <div
    28|              v-if="activeTab === tab.key"
    29|              class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500"
    30|            />
    31|          </button>
    32|        </div>
    33|
    34|        <!-- Form -->
    35|        <div class="p-8">
    36|          <!-- Error Message -->
    37|          <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
    38|            {{ error }}
    39|          </div>
    40|
    41|          <!-- Login Form -->
    42|          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-4">
    43|            <div>
    44|              <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
    45|              <input
    46|                v-model="loginForm.username"
    47|                type="text"
    48|                required
    49|                placeholder="请输入用户名"
    50|                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 transition-colors"
    51|              />
    52|            </div>
    53|            <div>
    54|              <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
    55|              <input
    56|                v-model="loginForm.password"
    57|                type="password"
    58|                required
    59|                placeholder="请输入密码"
    60|                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 transition-colors"
    61|              />
    62|            </div>
    63|            <button
    64|              type="submit"
    65|              :disabled="loading"
    66|              class="w-full btn-primary text-white py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
    67|            >
    68|              <span v-if="loading" class="flex items-center justify-center">
    69|                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
    70|                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
    71|                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
    72|                </svg>
    73|                登录中...
    74|              </span>
    75|              <span v-else>登录</span>
    76|            </button>
    77|          </form>
    78|
    79|          <!-- Register Form -->
    80|          <form v-else @submit.prevent="handleRegister" class="space-y-4">
    81|            <div>
    82|              <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
    83|              <input
    84|                v-model="registerForm.username"
    85|                type="text"
    86|                required
    87|                placeholder="请输入用户名"
    88|                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 transition-colors"
    89|              />
    90|            </div>
    91|            <div>
    92|              <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
    93|              <input
    94|                v-model="registerForm.email"
    95|                type="email"
    96|                required
    97|                placeholder="请输入邮箱"
    98|                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 transition-colors"
    99|              />
   100|            </div>
   101|            <div>
   102|              <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
   103|              <input
   104|                v-model="registerForm.password"
   105|                type="password"
   106|                required
   107|                placeholder="请输入密码"
   108|                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 transition-colors"
   109|              />
   110|            </div>
   111|            <div>
   112|              <label class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
   113|              <input
   114|                v-model="registerForm.confirmPassword"
   115|                type="password"
   116|                required
   117|                placeholder="请再次输入密码"
   118|                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-primary-500 transition-colors"
   119|              />
   120|            </div>
   121|            <button
   122|              type="submit"
   123|              :disabled="loading"
   124|              class="w-full btn-primary text-white py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed"
   125|            >
   126|              <span v-if="loading" class="flex items-center justify-center">
   127|                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
   128|                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
   129|                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
   130|                </svg>
   131|                注册中...
   132|              </span>
   133|              <span v-else>注册</span>
   134|            </button>
   135|          </form>
   136|        </div>
   137|      </div>
   138|
   139|      <!-- Footer -->
   140|      <p class="text-center text-white/60 text-sm mt-6">
   141|        基于知识图谱的地理旅游知识问答系统
   142|      </p>
   143|    </div>
   144|  </div>
   145|</template>
   146|
   147|<script setup lang="ts">
   148|import { ref, reactive } from 'vue'
   149|import { useRouter } from 'vue-router'
   150|import { useAuthStore } from '@/stores/auth'
   151|import { authApi } from '@/api/auth'
   152|
   153|const router = useRouter()
   154|const authStore = useAuthStore()
   155|
   156|const activeTab = ref<'login' | 'register'>('login')
   157|const loading = ref(false)
   158|const error = ref('')
   159|
   160|const tabs = [
   161|  { key: 'login' as const, label: '登录' },
   162|  { key: 'register' as const, label: '注册' }
   163|]
   164|
   165|const loginForm = reactive({
   166|  username: '',
   167|  password: ''
   168|})
   169|
   170|const registerForm = reactive({
   171|  username: '',
   172|  email: '',
   173|  password: '',
   174|  confirmPassword: ''
   175|})
   176|
   177|async function handleLogin() {
   178|  loading.value = true
   179|  error.value = ''
   180|  try {
   181|    const result = await authApi.login({
   182|      username: loginForm.username,
   183|      password: loginForm.password
   184|    })
   185|    authStore.setAuth(result.access_token, result.user)
   186|    router.push('/')
   187|  } catch (e: any) {
   188|    error.value = e.response?.data?.detail || '登录失败，请检查用户名和密码'
   189|  } finally {
   190|    loading.value = false
   191|  }
   192|}
   193|
   194|async function handleRegister() {
   195|  if (registerForm.password !== registerForm.confirmPassword) {
   196|    error.value = '两次输入的密码不一致'
   197|    return
   198|  }
   199|  loading.value = true
   200|  error.value = ''
   201|  try {
   202|    const result = await authApi.register({
   203|      username: registerForm.username,
   204|      email: registerForm.email,
   205|      password: registerForm.password
   206|    })
   207|    authStore.setAuth(result.access_token, result.user)
   208|    router.push('/')
   209|  } catch (e: any) {
   210|    error.value = e.response?.data?.detail || '注册失败，请稍后重试'
   211|  } finally {
   212|    loading.value = false
   213|  }
   214|}
   215|</script>
   216|