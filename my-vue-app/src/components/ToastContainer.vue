<script setup>
import Toast from './Toast.vue'

const props = defineProps({
  toasts: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['toast-close'])

const handleToastClose = (id) => {
  emit('toast-close', id)
}
</script>

<template>
  <!-- Toast Container - Fixed position on the right side -->
  <div
    aria-live="assertive"
    class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6 z-50"
  >
    <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
      <TransitionGroup
        enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
        enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        class="space-y-4"
      >
        <Toast
          v-for="toast in toasts"
          :key="toast.id"
          :message="toast.message"
          :type="toast.type"
          :duration="toast.duration"
          @close="handleToastClose(toast.id)"
        />
      </TransitionGroup>
    </div>
  </div>
</template>