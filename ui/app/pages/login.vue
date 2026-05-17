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
            <button class="btn social-btn" type="button" @click="fillDemo('google')">
              <span class="social-ico">G</span>
              Continue with Google
            </button>
            <button class="btn social-btn" type="button" @click="fillDemo('facebook')">
              <span class="social-ico">f</span>
              Continue with Facebook
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
import logoUrl from '~/assets/digital_assets/logo.png?url'

const logo = logoUrl
const router = useRouter()

const showPassword = ref(false)
const form = reactive({
  email: '',
  password: '',
  remember: true
})

const canSubmit = computed(() => form.email.includes('@') && form.password.length >= 6)

function fillDemo(provider: 'google' | 'facebook') {
  form.email = provider === 'google' ? 'admin@bakedsushi.com' : 'social@bakedsushi.com'
  form.password = 'bakedsushi'
}

async function login() {
  if (!canSubmit.value) return
  await router.push('/dashboard')
}

function noop() {}
</script>
