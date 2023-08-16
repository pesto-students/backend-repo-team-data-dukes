local now = require "util.time".now;
local jid = require "util.jid"

-- mod_chat_marker.lua
local archive_store = module:get_option_string("archive_store", "archive");
local archive = module:open_store(archive_store, "archive");

-- Define the function that will handle incoming messages
function handle_message(event)
  local origin, stanza = event.origin, event.stanza 

  if stanza.attr.type == "chat" or stanza.attr.type == "normal" or stanza.attr.type == "reply" then 

    -- Check if the incoming message has a child element called "received" or "displayed"
    local chat_marker = stanza:get_child("received", "urn:xmpp:chat-markers:0") or stanza:get_child("displayed", "urn:xmpp:chat-markers:0")
    if chat_marker then
      -- If it does, archive the message and update the archive with the new status
      message_id = chat_marker.attr.id
      local executor, err = archive:find(origin.username, {
      key = message_id
    });
      key, old_stanza = executor()

      -- Remove markable child element from old stanza
      old_stanza:maptags(function(tag)
        if tag.name == "markable" then
          return nil
        end
        return tag
      end)

      -- Add the received or displayed element to the old_stanza
      if not old_stanza:get_child(chat_marker.name, chat_marker.attr.xmlns) then
        old_stanza:add_child(chat_marker)
      end

      local sender_username = jid.node(stanza.attr.to)  
      local replyer_jid = jid.bare(stanza.attr.from)

      -- Update the archive with the modified old_stanza

      -- received or displayed stanza from receiver to sender update
      updated_from, err = archive:set(origin.username, key, old_stanza, now(), stanza.attr.to)
      
      -- received or displayed stanza from send to receiver update
      updated_to, err1 = archive:set(sender_username, key, old_stanza, now(), replyer_jid)

      if updated_from and updated_to then
        return nil
      end
    end
  end
end

-- Hook into incoming messages to call our function
module:hook("message/bare", handle_message, 1);
