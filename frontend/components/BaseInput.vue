<template>
  <label class="field">
    <span>{{ label }}</span>
    <input
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    >
    <small v-if="error">{{ error }}</small>
  </label>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string
    label: string
    type?: string
    placeholder?: string
    error?: string
  }>(),
  {
    type: 'text',
    placeholder: '',
    error: '',
  },
)

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<style scoped>
.field {
  display: grid;
  gap: 8px;
  color: var(--color-text);
  font-weight: 600;
}

input {
  min-height: 46px;
  border: 1px solid rgba(244, 143, 177, 0.34);
  border-radius: var(--radius-md);
  background: white;
  color: var(--color-text);
  padding: 0 14px;
  outline: none;
}

input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(244, 143, 177, 0.18);
}

small {
  color: #b3261e;
  font-weight: 500;
}
</style>
