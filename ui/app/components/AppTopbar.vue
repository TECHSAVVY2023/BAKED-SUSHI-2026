<template>
  <header class="topbar">
    <div class="mx-auto flex w-full max-w-7xl flex-wrap items-center gap-4 px-4 py-4 sm:px-6 lg:flex-nowrap">
      <div class="min-w-0 flex-1">
        <slot name="left" />
      </div>

      <div
        class="order-3 flex w-full justify-center lg:order-none lg:w-auto lg:flex-1"
        role="navigation"
        aria-label="Top navigation"
      >
        <slot name="center" />
      </div>

      <div class="ml-auto flex flex-wrap items-center justify-end gap-3 lg:flex-1">
        <slot name="right" />
      </div>
    </div>
  </header>
</template>
