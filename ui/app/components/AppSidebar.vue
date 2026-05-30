<template>
  <aside class="sidebar" :class="variantClass" :style="sidebarStyle" aria-label="Sidebar navigation">
    <div class="side-card" :style="cardStyle">
      <div class="brand" :style="brandStyle">
        <slot name="brand" />
      </div>

      <nav class="nav" :style="navStyle">
        <NuxtLink
          v-for="item in items"
          :key="item.to"
          class="link"
          :style="linkStyle"
          :to="item.to"
          :aria-label="item.label"
        >
          <span class="dot" aria-hidden="true" />
          <span class="label">{{ item.label }}</span>
        </NuxtLink>
      </nav>

      <div class="footer" :style="footerStyle">
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

const sidebarStyle = computed(() => {
  const base = {
    display: 'block',
    width: '248px',
    zIndex: '90',
    color: 'rgba(20, 12, 10, 0.88)'
  }

  if ((props.variant ?? 'sticky') === 'fixed') {
    return {
      ...base,
      position: 'fixed',
      left: '16px',
      top: '16px',
      bottom: '16px'
    }
  }

  return {
    ...base,
    position: 'sticky',
    top: '16px',
    height: 'calc(100vh - 32px)'
  }
})

const cardStyle = {
  display: 'flex',
  height: '100%',
  flexDirection: 'column',
  overflow: 'hidden',
  border: '1px solid rgba(242, 161, 170, 0.34)',
  borderRadius: '24px',
  background:
    'radial-gradient(420px 220px at 20% 0%, rgba(242, 124, 134, 0.16), transparent 58%), linear-gradient(180deg, rgba(255, 250, 251, 0.96), rgba(255, 244, 246, 0.9))',
  boxShadow: '0 24px 70px rgba(20, 12, 10, 0.12)',
  backdropFilter: 'blur(18px)'
}

const brandStyle = {
  padding: '18px',
  borderBottom: '1px solid rgba(20, 12, 10, 0.08)'
}

const navStyle = {
  display: 'grid',
  gap: '8px',
  padding: '14px'
}

const linkStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '12px',
  padding: '10px 12px',
  borderRadius: '14px',
  border: '1px solid rgba(20, 12, 10, 0.1)',
  background: 'rgba(255, 255, 255, 0.82)',
  color: 'rgba(20, 12, 10, 0.9)',
  fontWeight: '800',
  textDecoration: 'none'
}

const footerStyle = {
  marginTop: 'auto',
  padding: '16px 18px 18px',
  borderTop: '1px solid rgba(20, 12, 10, 0.08)',
  color: 'rgba(20, 12, 10, 0.58)',
  fontSize: '12px',
  fontWeight: '700',
  lineHeight: '1.4'
}
</script>
