<template>
  <label class="field">
    <span :id="labelId">{{ label }}</span>
    <input
      :id="inputId"
      :value="modelValue"
      :type="type"
      :name="name"
      :placeholder="placeholder"
      :inputmode="inputmode"
      :autocomplete="autocomplete"
      :maxlength="maxlength"
      :aria-labelledby="labelId"
      :aria-invalid="error ? 'true' : 'false'"
      :aria-describedby="error ? errorId : undefined"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    >
    <small v-if="error" :id="errorId" role="alert">{{ error }}</small>
  </label>
</template>

<script setup lang="ts">
import { computed, useId } from 'vue'

const props = withDefaults(
  defineProps<{
    id?: string
    modelValue: string
    label: string
    name?: string
    type?: string
    placeholder?: string
    error?: string
    inputmode?: string
    autocomplete?: string
    maxlength?: number
  }>(),
  {
    id: '',
    type: 'text',
    name: '',
    placeholder: '',
    error: '',
    inputmode: 'text',
    autocomplete: '',
    maxlength: undefined,
  },
)

defineEmits<{
  'update:modelValue': [value: string]
}>()

const generatedId = useId()
const inputId = computed(() => props.id || `input-${generatedId}`)
const labelId = computed(() => `${inputId.value}-label`)
const errorId = computed(() => `${inputId.value}-error`)
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
