<template>
  <div class="auth-page">
    <div class="backdrop" aria-hidden="true" />

    <section class="modal" aria-labelledby="login-title">
      <NuxtLink class="close" to="/" aria-label="Close login">
        <span>&times;</span>
      </NuxtLink>

      <div class="modal-inner">
        <div class="panel left">
          <div class="brand">
            <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
            <div>
              <div class="brand-name">Baked Sushi</div>
              <div class="brand-tag">Admin access</div>
            </div>
          </div>

          <h1 id="login-title" class="title">Welcome back</h1>
          <p class="sub">Sign in to manage orders, products, and your mock dashboard.</p>

          <div class="social">
            <button class="social-btn" type="button" @click="fillDemo('google')">
              <span class="social-ico">
                <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
                </svg>
              </span>
              Continue with Google
            </button>
            <button class="social-btn" type="button" @click="fillDemo('microsoft')">
              <span class="social-ico">
                <svg viewBox="0 0 23 23" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
                  <path fill="#F25022" d="M1 1h10v10H1z"/>
                  <path fill="#7FBA00" d="M12 1h10v10H12z"/>
                  <path fill="#00A4EF" d="M1 12h10v10H1z"/>
                  <path fill="#FFB900" d="M12 12h10v10H12z"/>
                </svg>
              </span>
              Continue with Microsoft
            </button>
          </div>

          <div class="divider" aria-hidden="true">
            <div class="divider-line" />
            <div class="divider-text">or use email</div>
            <div class="divider-line" />
          </div>

          <form class="form" @submit.prevent="login">
            <label class="field">
              <span class="label">Email</span>
              <div class="input-wrap">
                <input
                  v-model.trim="form.email"
                  class="input"
                  type="email"
                  autocomplete="email"
                  placeholder="you@example.com"
                />
              </div>
            </label>

            <label class="field">
              <span class="label">Password</span>
              <div class="input-wrap">
                <input
                  v-model="form.password"
                  class="input"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  placeholder="Enter your password"
                />
                <button class="ghost" type="button" @click="showPassword = !showPassword">
                  {{ showPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </label>

            <div class="row">
              <label class="check">
                <input v-model="form.remember" type="checkbox" />
                <span>Remember me</span>
              </label>
              <a class="link" href="#" @click.prevent="noop">Forgot password?</a>
            </div>

            <button class="btn primary" type="submit" :disabled="!canSubmit">Sign in</button>
          </form>

          <p class="legal">Demo login only. Use any valid-looking email and a password with at least 6 characters.</p>
        </div>

        <div class="panel right">
          <div class="right-glow" aria-hidden="true" />
          <div class="right-content">
            <img class="right-logo" :src="logo" alt="Baked Sushi logo" />
            <div class="right-title">Freshly baked. Ready to manage.</div>
            <p class="right-sub">
              Keep track of orders, update products, and monitor activity from one clean admin space.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/assets/digital_assets/logo.jpg?url'

const logo = logoUrl
const router = useRouter()

const showPassword = ref(false)
const form = reactive({
  email: '',
  password: '',
  remember: true
})

const canSubmit = computed(() => form.email.includes('@') && form.password.length >= 6)

function fillDemo(provider: 'google' | 'microsoft') {
  form.email = provider === 'google' ? 'admin@bakedsushi.com' : 'social@bakedsushi.com'
  form.password = 'bakedsushi'
}

async function login() {
  if (!canSubmit.value) return
  await router.push('/dashboard')
}

function noop() {}
</script>
