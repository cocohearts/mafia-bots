<script>
  import { onMount } from 'svelte';
  import { socket } from '$lib/socketio';
  import { cn } from '$lib/utils';

  import Button from '$lib/components/ui/button/button.svelte';
  import Input from '$lib/components/ui/input/input.svelte';

  import { GithubIcon, PlusIcon } from 'svelte-feather-icons';

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
        [new Date(), 'system', 'welcome to mafia bots!'],
      ];
    });

    // Game message types
    /* const handlers = {
      game_start: (data) => {
        messages = [
          ...messages,
          [
            new Date(),
            'system',
            `The game has started with <b>${data.length}</b> players.`,
          ],
        ];
        players = data;
      },
    };

    Object.entries(handlers).forEach(([handler_type, callback]) => {
      socket.on(handler_type, (data) => callback(data));
    }); */

    socket.on('message', (data) => {
      let raw_timestamp = data.timestamp;
      data.timestamp = new Date(raw_timestamp * 1000);
      messages = [[data.timestamp, data.author, data.content], ...messages];
    });

    return () => {
      socket.off('connect');
      socket.off('message');
      Object.keys(handlers).forEach((handler_type) => socket.off(handler_type));
    };
  }, []);

  // Page variables
  let messages = [];
  let players = [];
</script>

<div class="flex h-screen flex-col">
  <!-- Navbar -->
  <div class="flex w-full bg-neutral-100 p-4">
    <div class="mr-auto">
      <span class="font-bold">mafia-bots</span>
    </div>
    <a href="https://github.com/cocohearts/mafia-bots"><GithubIcon /></a>
  </div>

  <!-- Main body -->
  <div class="flex flex-grow divide-x overflow-y-hidden">
    <div class="flex w-80 flex-col gap-2 p-2">
      <Button class="flex gap-2" on:click={() => socket.emit('new_game')}>
        <PlusIcon /><span>New game</span></Button
      >
      <Button variant="outline" on:click={() => (messages = [])}
        >Clear chat</Button
      >

      <!-- Game status -->
      <div class="p-2">
        <div>Day 0</div>

        <div class="mt-4 flex gap-2 text-sm">
          {#each players as { name, role, alignment }}
            <div class="flex items-center gap-4">
              <span>{name} ({role})</span>
              <div
                class={cn(
                  'ml-auto h-4 w-4 rounded-full',
                  alignment === 'Mafia' ? 'bg-red-600' : 'bg-blue-600',
                )}
              ></div>
            </div>
          {/each}
        </div>
      </div>
    </div>

    <!-- Chat column -->
    <div class="flex w-full flex-col">
      <!-- Chat messages -->
      <table
        class="flex flex-grow border-spacing-2 flex-col-reverse overflow-y-auto"
      >
        {#each messages as [timestamp, author, content]}
          <tr class="px-4 py-1 align-top text-sm">
            <td class="text-muted-foreground whitespace-pre"
              >{timestamp.toLocaleTimeString()}</td
            >
            <td class="text-muted-foreground px-2">{author.split('-')[0]}</td>
            <td>{@html content}</td>
          </tr>
        {/each}
      </table>

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
