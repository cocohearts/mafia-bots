<script>
  import Button from '$lib/components/ui/button/button.svelte';
  import Input from '$lib/components/ui/input/input.svelte';

  import { io } from 'socket.io-client';
  import { onMount } from 'svelte';

  onMount(() => {
    const socket = io('ws://127.0.0.1:5000');

    return () => socket.disconnect();
  }, []);
</script>

<div class="flex h-screen flex-col">
  <!-- Navbar -->
  <div class="w-full bg-neutral-100 p-4">
    <div>
      <span class="font-bold">mafia</span>
    </div>
  </div>

  <!-- Main body -->
  <div class="flex flex-grow divide-x">
    <div class="w-80"></div>

    <!-- Chat column -->
    <div class="flex w-full flex-col">
      <!-- Chat messages -->
      <div class="flex-grow"></div>

      <!-- Chat input -->
      <div class="flex gap-2 p-2">
        <Input placeholder="Chat with the group..." />
        <Button>Send</Button>
      </div>
    </div>

    <div class="w-80"></div>
  </div>
</div>
