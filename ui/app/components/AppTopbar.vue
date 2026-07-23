<template>
  <header class="topbar">
    <div class="flex w-full h-full items-center gap-4 px-5">
      <div class="min-w-0 flex-1 flex items-center gap-3">
        <slot name="left" />
      </div>

      <div
        class="flex items-center"
        role="navigation"
        aria-label="Top navigation"
      >
        <slot name="center" />
      </div>

      <div class="flex flex-wrap items-center justify-end gap-3">
        <slot name="right" />
      </div>
    </div>
  </header>
</template>
