<script>
  import { onMount } from 'svelte';

  import Button from '$lib/components/ui/button/button.svelte';
  import Input from '$lib/components/ui/input/input.svelte';
  import { socket } from '$lib/socketio';

  let chatInput;
  const sendChatMessage = () => {
    console.log(chatInput);
    socket.emit('message', chatInput);
  };

  onMount(() => {
    socket.on('connect', () => {
      messages = [
        ...messages,
        {
          timestamp: new Date(),
          author: 'system',
          content: `socket.io connected, sid: ${socket.id}`,
        },
      ];
    });

    return () => socket.off('connect');
  }, []);

  // Page variables
  let messages = [];
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
      <div class="flex flex-grow flex-col">
        {#each messages as message}
          <div class="flex gap-2 px-4 py-1 text-sm">
            <span class="text-muted-foreground"
              >{message.timestamp.toLocaleTimeString()}</span
            >
            <span class="text-muted-foreground">{message.author}</span>
            <span>{message.content}</span>
          </div>
        {/each}
      </div>

      <!-- Chat input -->
      <div class="flex gap-2 p-2">
        <Input
          on:keydown={(e) => e.key === 'Enter' && sendChatMessage()}
          bind:value={chatInput}
          placeholder="Chat with the group..."
        />
        <Button on:click={sendChatMessage}>Send</Button>
      </div>
    </div>
  </div>
</div>
