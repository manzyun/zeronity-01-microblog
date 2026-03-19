<script lang="ts">
  import { actorApi } from '../lib/api';

  let { onLoginSuccess } = $props<{ onLoginSuccess: (user: any) => void }>();

  let username = $state('');
  let password = $state('');
  let isRegistering = $state(false);
  let error = $state('');
  let isLoading = $state(false);

  async function handleSubmit() {
    if (!username || !password) return;
    isLoading = true;
    error = '';
    try {
      let user;
      if (isRegistering) {
        user = await actorApi.register(username, password);
        // Automatically login after registration or ask to login?
        // Let's just login for simplicity.
        user = await actorApi.login(username, password);
      } else {
        user = await actorApi.login(username, password);
      }
      onLoginSuccess(user);
    } catch (e: any) {
      error = e.message || 'Authentication failed';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="max-w-md mx-auto w-full px-4 pt-20">
  <div class="card p-8 shadow-2xl">
    <h1 class="text-3xl font-bold text-center mb-8 text-gruvbox-light0">Zeronity</h1>
    
    {#if error}
      <div class="bg-gruvbox-red/20 border border-gruvbox-red text-gruvbox-red p-3 rounded-md mb-6 text-sm">
        {error}
      </div>
    {/if}

    <div class="flex flex-col gap-4">
      <input 
        bind:value={username}
        placeholder="Username"
        class="input p-3"
        disabled={isLoading}
      />
      <input 
        type="password"
        bind:value={password}
        placeholder="Password"
        class="input p-3"
        disabled={isLoading}
      />
      
      <button 
        onclick={handleSubmit}
        class="bg-gruvbox-blue text-gruvbox-light0 font-bold py-3 rounded-md hover:bg-opacity-80 transition-all mt-4 disabled:opacity-50"
        disabled={isLoading}
      >
        {isLoading ? 'Processing...' : (isRegistering ? 'Sign Up' : 'Log In')}
      </button>

      <div class="text-center mt-6 text-sm">
        <button 
          onclick={() => isRegistering = !isRegistering}
          class="text-gruvbox-aqua hover:underline"
        >
          {isRegistering ? 'Already have an account? Log in' : "Don't have an account? Sign up"}
        </button>
      </div>
    </div>
  </div>
</div>
