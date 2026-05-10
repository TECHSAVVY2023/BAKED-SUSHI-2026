<template>
  <header class="topbar">
    <div class="container topbar-inner">
      <div class="left">
        <slot name="left" />
      </div>

      <div class="center" role="navigation" aria-label="Top navigation">
        <slot name="center" />
      </div>

      <div class="right">
        <slot name="right" />
      </div>
    </div>
  </header>
</template>
