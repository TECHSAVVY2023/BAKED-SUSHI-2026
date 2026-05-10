<template>
  <div class="auth-page">
    <div class="backdrop" aria-hidden="true" />

    <section class="modal" role="dialog" aria-modal="true" aria-label="Login">
      <NuxtLink class="close" to="/" aria-label="Close">
        <span aria-hidden="true">×</span>
      </NuxtLink>

      <div class="modal-inner">
        <div class="panel left">
          <div class="brand">
            <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
            <div class="brand-text">
              <div class="brand-name">Baked Sushi</div>
              <div class="brand-tag">Scoop | Wrap | Munch | Repeat</div>
            </div>
          </div>

          <h1 class="title">Welcome back</h1>
          <p class="sub">Sign in to continue to your account</p>

          <div class="social">
            <button class="btn social-btn" type="button">
              <span class="social-ico" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M21.6 12.27c0-.68-.06-1.35-.18-2H12v3.78h5.38a4.6 4.6 0 0 1-1.99 3.02v2.5h3.22c1.88-1.73 2.99-4.29 2.99-7.3Z"
                    fill="currentColor"
                    opacity=".9"
                  />
                  <path
                    d="M12 22c2.7 0 4.96-.9 6.61-2.43l-3.22-2.5c-.9.6-2.06.95-3.39.95-2.61 0-4.82-1.76-5.61-4.12H3.06v2.57A10 10 0 0 0 12 22Z"
                    fill="currentColor"
                    opacity=".8"
                  />
                  <path
                    d="M6.39 13.9a5.98 5.98 0 0 1 0-3.8V7.53H3.06a10 10 0 0 0 0 8.94l3.33-2.57Z"
                    fill="currentColor"
                    opacity=".7"
                  />
                  <path
                    d="M12 5.98c1.47 0 2.79.5 3.83 1.5l2.87-2.87C16.95 2.9 14.69 2 12 2A10 10 0 0 0 3.06 7.53l3.33 2.57C7.18 7.74 9.39 5.98 12 5.98Z"
                    fill="currentColor"
                    opacity=".6"
                  />
                </svg>
              </span>
              Continue with Google
            </button>

            <button class="btn social-btn" type="button">
              <span class="social-ico" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M2 2h9v9H2V2Z" fill="currentColor" opacity=".9" />
                  <path d="M13 2h9v9h-9V2Z" fill="currentColor" opacity=".75" />
                  <path d="M2 13h9v9H2v-9Z" fill="currentColor" opacity=".75" />
                  <path d="M13 13h9v9h-9v-9Z" fill="currentColor" opacity=".9" />
                </svg>
              </span>
              Continue with Microsoft
            </button>
          </div>

          <div class="divider" role="separator">
            <span class="divider-line" aria-hidden="true" />
            <span class="divider-text">or</span>
            <span class="divider-line" aria-hidden="true" />
          </div>

          <form class="form" @submit.prevent="noop">
            <label class="field">
              <span class="label">Email</span>
              <input
                v-model="email"
                class="input"
                type="email"
                autocomplete="email"
                placeholder="you@example.com"
              />
            </label>

            <label class="field">
              <span class="label">Password</span>
              <div class="input-wrap">
                <input
                  v-model="password"
                  class="input"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  placeholder="••••••••"
                />
                <button class="ghost" type="button" @click="showPassword = !showPassword">
                  {{ showPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </label>

            <div class="row">
              <label class="check">
                <input v-model="remember" type="checkbox" />
                <span>Remember me</span>
              </label>
              <a class="link" href="#" @click.prevent="noop">Forgot password?</a>
            </div>

            <button class="btn primary" type="submit">Sign in</button>
          </form>

          <div class="legal">© {{ year }} Baked Sushi. All rights reserved.</div>
        </div>

        <div class="panel right">
          <div class="right-glow" aria-hidden="true" />
          <div class="right-content">
            <img class="right-logo" :src="logo" alt="" />
            <div class="right-title">Freshly baked happiness</div>
            <div class="right-sub">Pink Salmon base • gold accents • made with love</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/assets/digital_assets/logo.png?url'

const logo = logoUrl

const email = ref('')
const password = ref('')
const remember = ref(true)
const showPassword = ref(false)
const year = new Date().getFullYear()

function noop() {}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 20px;
  background: radial-gradient(1200px 600px at 20% 10%, rgba(250, 128, 114, 0.24), transparent 55%),
    radial-gradient(900px 500px at 80% 90%, rgba(214, 166, 74, 0.18), transparent 55%),
    linear-gradient(180deg, rgba(255, 239, 242, 1), rgba(255, 248, 250, 1));
  color: rgba(20, 12, 10, 0.92);
}

.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(20, 12, 10, 0.35);
  backdrop-filter: blur(10px);
}

.modal {
  position: relative;
  z-index: 2;
  width: min(980px, 96vw);
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 40px 120px rgba(20, 12, 10, 0.45);
  overflow: hidden;
}

.close {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 4;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  text-decoration: none;
  color: rgba(20, 12, 10, 0.8);
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(20, 12, 10, 0.12);
}

.close span {
  font-size: 22px;
  line-height: 1;
  transform: translateY(-1px);
}

.modal-inner {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  min-height: 560px;
  background: rgba(255, 255, 255, 0.8);
}

.panel {
  position: relative;
}

.left {
  padding: 34px 34px 28px;
  background: rgba(255, 255, 255, 0.92);
}

.right {
  background: linear-gradient(135deg, rgba(250, 128, 114, 1), rgba(214, 166, 74, 0.92));
  color: rgba(255, 255, 255, 0.95);
  overflow: hidden;
}

.right::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.16), transparent 42%),
    radial-gradient(circle at 80% 40%, rgba(255, 255, 255, 0.12), transparent 46%),
    radial-gradient(circle at 65% 85%, rgba(255, 255, 255, 0.1), transparent 48%);
  opacity: 0.9;
}

.right-glow {
  position: absolute;
  inset: -80px;
  background: radial-gradient(closest-side at 50% 30%, rgba(255, 255, 255, 0.18), transparent 62%);
  filter: blur(10px);
  opacity: 0.9;
}

.right-content {
  position: relative;
  height: 100%;
  padding: 34px;
  display: grid;
  align-content: center;
  justify-items: center;
  text-align: center;
  gap: 14px;
}

.right-logo {
  width: min(320px, 72%);
  aspect-ratio: 1 / 1;
  object-fit: contain;
  filter: drop-shadow(0 18px 40px rgba(20, 12, 10, 0.35));
}

.right-title {
  font-weight: 950;
  letter-spacing: -0.02em;
  font-size: 22px;
}

.right-sub {
  opacity: 0.92;
  font-size: 14px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 245, 247, 0.9);
}

.brand-name {
  font-weight: 950;
  line-height: 1.05;
}

.brand-tag {
  font-size: 12px;
  opacity: 0.72;
}

.title {
  margin-top: 20px;
  font-size: 28px;
  letter-spacing: -0.02em;
  font-weight: 950;
}

.sub {
  margin-top: 6px;
  color: rgba(20, 12, 10, 0.62);
  font-size: 14px;
}

.social {
  margin-top: 18px;
  display: grid;
  gap: 10px;
}

.btn {
  height: 44px;
  border-radius: 14px;
  padding: 0 14px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.8);
  color: rgba(20, 12, 10, 0.88);
  font-weight: 850;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  transition: transform 0.08s ease, box-shadow 0.12s ease, background 0.12s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(20, 12, 10, 0.12);
}

.social-btn {
  justify-content: flex-start;
}

.social-ico {
  width: 28px;
  height: 28px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: rgba(250, 128, 114, 0.14);
  color: rgba(250, 128, 114, 0.95);
  border: 1px solid rgba(214, 166, 74, 0.28);
}

.social-ico svg {
  width: 18px;
  height: 18px;
}

.divider {
  margin: 18px 0 12px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 12px;
}

.divider-line {
  height: 1px;
  background: rgba(20, 12, 10, 0.12);
}

.divider-text {
  font-size: 12px;
  font-weight: 850;
  color: rgba(20, 12, 10, 0.58);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.form {
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 8px;
}

.label {
  font-size: 12px;
  font-weight: 900;
  color: rgba(20, 12, 10, 0.72);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.input-wrap {
  position: relative;
}

.input {
  width: 100%;
  height: 44px;
  padding: 0 14px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.14);
  background: rgba(255, 255, 255, 0.92);
  color: rgba(20, 12, 10, 0.9);
  outline: none;
  transition: box-shadow 0.12s ease, border-color 0.12s ease;
}

.input:focus {
  border-color: rgba(250, 128, 114, 0.8);
  box-shadow: 0 0 0 4px rgba(250, 128, 114, 0.18);
}

.ghost {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  height: 30px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.7);
  font-weight: 900;
  color: rgba(20, 12, 10, 0.72);
  cursor: pointer;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.check {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  color: rgba(20, 12, 10, 0.7);
  font-size: 13px;
}

.check input {
  width: 16px;
  height: 16px;
  accent-color: rgb(250, 128, 114);
}

.link {
  font-size: 13px;
  font-weight: 900;
  color: rgba(250, 128, 114, 0.98);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.primary {
  margin-top: 2px;
  background: linear-gradient(135deg, rgba(250, 128, 114, 1), rgba(214, 166, 74, 1));
  border-color: rgba(255, 255, 255, 0.22);
  color: rgba(255, 255, 255, 0.96);
  box-shadow: 0 20px 40px rgba(250, 128, 114, 0.22);
}

.legal {
  margin-top: 16px;
  font-size: 12px;
  color: rgba(20, 12, 10, 0.42);
}

@media (max-width: 860px) {
  .modal-inner {
    grid-template-columns: 1fr;
  }

  .right {
    min-height: 240px;
  }

  .left {
    padding: 26px 20px 22px;
  }

  .right-content {
    padding: 26px 20px;
  }
}
</style>
