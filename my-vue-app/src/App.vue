<script setup>
import { ref, provide } from 'vue'
import Budgeting from './views/Budgeting.vue';
import ToastContainer from './components/ToastContainer.vue';

const toasts = ref([])
let nextId = 1

// Provide toast functionality to all child components
provide('showToast', (message, type = 'error', duration = 5000) => {
  const id = nextId++
  const toast = {
    id,
    message,
    type,
    duration
  }

  toasts.value.push(toast)

  // Remove toast after it closes
  setTimeout(() => {
    removeToast(id)
  }, duration + 300) // Add 300ms for transition
})

const removeToast = (id) => {
  const index = toasts.value.findIndex(toast => toast.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

const handleToastClose = (id) => {
  removeToast(id)
}
</script>

<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- App Header -->
    <header class="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo and Title -->
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
              </svg>
            </div>
            <h1 class="text-xl font-bold text-gray-900">Budget Master</h1>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Budgeting />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="text-center text-sm text-gray-500">
          <p>&copy; 2024 Budget Master. Built with Vue.js and FastAPI.</p>
        </div>
      </div>
    </footer>

    <!-- Toast Container -->
    <ToastContainer :toasts="toasts" @toast-close="handleToastClose" />
  </div>
</template>

<style>
/* Global styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Smooth transitions */
.transition {
  transition: all 0.2s ease-in-out;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
