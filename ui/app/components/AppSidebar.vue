<template>
  <aside class="sidebar" :class="variantClass" aria-label="Sidebar navigation">
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
          <span class="dot" aria-hidden="true" />
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
type SidebarItem = { label: string; to: string }

const props = defineProps<{
  items: SidebarItem[]
  variant?: 'sticky' | 'fixed'
}>()

const variantClass = computed(() => `is-${props.variant ?? 'sticky'}`)
</script>
