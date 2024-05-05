<script>
  import { onMount } from 'svelte';
  import { socket } from '$lib/socketio';

  import Button from '$lib/components/ui/button/button.svelte';
  import Input from '$lib/components/ui/input/input.svelte';

  import { PlusIcon } from 'svelte-feather-icons';

  let chatInputElement;
  const sendChatMessage = () => {
    socket.emit('message', chatInputElement.value);
    chatInputElement.value = '';
  };

  onMount(() => {
    // Socket things
    socket.on('connect', () => {
      console.log(`socket.io connected, id: ${socket.id}`);
      socket.emit('set_username', localStorage.getItem('username'));

      // Welcome message
      messages = [
        ...messages,
        {
          timestamp: new Date(),
          author: 'system',
          content: 'welcome to mafia bots!',
        },
      ];
    });

    socket.on('message', (data) => {
      let raw_timestamp = data.timestamp;
      data.timestamp = new Date(raw_timestamp * 1000);
      messages = [...messages, data];
    });

    return () => {
      socket.off('connect');
      socket.off('message');
    };
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
    <div class="w-80 p-2">
      <Button
        class="flex w-full gap-2"
        variant="outline"
        on:click={() => socket.emit('new_game')}
      >
        <PlusIcon /><span>New game</span></Button
      >
    </div>

    <!-- Chat column -->
    <div class="flex w-full flex-col">
      <!-- Chat messages -->
      <div class="flex flex-grow flex-col">
        {#each messages as message}
          <div class="flex gap-2 px-4 py-1 text-sm">
            <span class="text-muted-foreground"
              >{message.timestamp.toLocaleTimeString()}</span
            >
            <span class="text-muted-foreground"
              >{message.author.split('-')[0]}</span
            >
            <span>{message.content}</span>
          </div>
        {/each}
      </div>

      <!-- Chat input -->
      <div class="flex gap-2 p-2">
        <Input
          on:keydown={(e) => e.key === 'Enter' && sendChatMessage()}
          placeholder="Chat with the group..."
          bind:this={chatInputElement}
        />
        <Button on:click={sendChatMessage}>Send</Button>
      </div>
    </div>
  </div>
</div>
