<script lang="ts">
  import Login from '../components/Login.svelte';
  import Feed from '../components/Feed.svelte';
  import { onMount } from 'svelte';

  let user = $state(null as any);
  let isCheckingAuth = $state(true);

  onMount(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      user = JSON.parse(savedUser);
    }
    isCheckingAuth = false;
  });

  function handleLoginSuccess(loggedInUser: any) {
    user = loggedInUser;
    localStorage.setItem('user', JSON.stringify(user));
  }

  function handleLogout() {
    user = null;
    localStorage.removeItem('user');
  }
</script>

<div class="min-h-screen flex flex-col bg-gruvbox-dark0 text-gruvbox-light1">
  {#if isCheckingAuth}
    <div class="flex-grow flex items-center justify-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gruvbox-blue"></div>
    </div>
  {:else if !user}
    <div class="flex-grow flex items-center justify-center">
      <Login onLoginSuccess={handleLoginSuccess} />
    </div>
  {:else}
    <header class="bg-gruvbox-dark1 border-b border-gruvbox-dark2 p-4 sticky top-0 z-10 shadow-md">
      <div class="max-w-4xl mx-auto flex justify-between items-center px-4">
        <h1 class="text-2xl font-bold text-gruvbox-light0 tracking-wider">Zeronity</h1>
        
        <div class="flex items-center gap-6">
          <div class="hidden sm:flex items-center gap-2">
            <div class="w-8 h-8 rounded-full bg-gruvbox-dark3 flex items-center justify-center font-bold text-gruvbox-light0 text-xs">
              {user.username?.[0].toUpperCase()}
            </div>
            <span class="text-gruvbox-light1 text-sm font-medium">@{user.username}</span>
          </div>
          <button 
            onclick={handleLogout}
            class="text-gruvbox-light4 hover:text-gruvbox-red transition-colors text-sm font-bold"
          >
            Log Out
          </button>
        </div>
      </div>
    </header>

    <main class="flex-grow bg-gruvbox-dark0 pt-8 pb-20">
      <Feed />
    </main>

    <nav class="sm:hidden fixed bottom-0 left-0 right-0 bg-gruvbox-dark1 border-t border-gruvbox-dark2 flex justify-around p-3 shadow-xl z-20">
      <button class="text-gruvbox-light1">Home</button>
      <button class="text-gruvbox-light1">Search</button>
      <button class="text-gruvbox-light1">Post</button>
      <button class="text-gruvbox-light1">Profile</button>
    </nav>
  {/if}
</div>
