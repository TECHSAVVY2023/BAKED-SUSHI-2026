<template>
  <aside class="sidebar" :class="variantClass" :style="sidebarStyle" aria-label="Sidebar navigation">
    <div class="side-card">
      <div class="brand">
        <slot name="brand" />
      </div>

      <nav class="nav">
        <NuxtLink
          v-for="item in items"
          :key="item.to"
          class="link"
          :to="item.to"
          :aria-label="item.label"
        >
          <!-- Icon wrapper with clean inline SVGs -->
          <span class="icon-wrap" aria-hidden="true">
            <svg v-if="item.to.includes('dashboard')" class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z" />
            </svg>
            <svg v-else-if="item.to.includes('orders')" class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            <svg v-else-if="item.to.includes('products')" class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            <span v-else class="dot" />
          </span>
          <span class="label">{{ item.label }}</span>
        </NuxtLink>
      </nav>

      <div class="footer">
        <slot name="footer" />
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type SidebarItem = { label: string; to: string }

const props = defineProps<{
  items: SidebarItem[]
  variant?: 'sticky' | 'fixed'
}>()

const variantClass = computed(() => `is-${props.variant ?? 'sticky'}`)

const sidebarStyle = computed(() => {
  const base = {
    display: 'block',
    width: '260px',
    zIndex: '90',
    color: 'rgba(20, 12, 10, 0.88)'
  }

  if ((props.variant ?? 'sticky') === 'fixed') {
    return {
      ...base,
      position: 'fixed',
      left: '0',
      top: '0',
      bottom: '0'
    }
  }

  return {
    ...base,
    position: 'sticky',
    top: '0',
    height: '100vh'
  }
})
</script>
