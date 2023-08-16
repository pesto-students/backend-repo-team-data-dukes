-- File: mod_remove_member_on_exit.lua
-- Prosody module to remove a user from the member list and remove their affiliation when they exit the room

-- Load required modules
local jid = require "util.jid";
local muc_component_host = module:get_option_string("MUC_COMPONENT");
local jid_split = require "util.jid".split;
local jid_bare = require "util.jid".bare;
local st = require"util.stanza";

module:log("info", "testing module loaded");

local get_room_from_jid = function (room_jid)
   local _, host = jid_split(room_jid);
   local component = hosts[host];
   module:log("info", "component: %s", component);
   if component then
       local muc = component.modules.muc;
       module:log("info", "muc: %s", muc);
       if muc and rawget(muc,"rooms") then
           -- We're running 0.9.x or 0.10 (old MUC API)
           return muc.rooms[room_jid];
       elseif muc and rawget(muc,"get_room_from_jid") then
           -- We're running >0.10 (new MUC API)
           module:log("info", "muc: %s", muc);
           return muc.get_room_from_jid(room_jid);
       else
           return nil;
       end
   end
 end

-- Function to remove a user from the member list and remove their affiliation

function remove_member_from_room(room, user)
   module:log("info", "user %s", user);
   local user_jid = jid_bare(user);
   local success, error, condition = room:set_affiliation(true, user_jid, nil);
   if not success then
       module:log("info", "couldn't kick the user, error: %s, condition: %s", error, condition);
       return nil;
   end
   module:log("info", "User %s Removed From %s", user, room);

   -- Send presence stanza to the user
   local presence = st.presence({ to = user_jid, type = "unavailable", id = "exit-room" });
   module:send(presence);
   return nil;
end

-- Function to handle presence stanzas
function mod_remove_member_on_exit_presence_handler(event)
   local session = event.origin;
   local room = event.room;
   local stanza = event.stanza;
   local room_jid = stanza.attr.to;
   local room = get_room_from_jid(room_jid);
   module:log("info", "ROOM : %s", room);

   if room == nil then
       return nil;
   end
   if stanza.attr.type == "unavailable" and stanza.attr.id == "exit-room" then
       if room then
           remove_member_from_room(room, stanza.attr.from);
       end
   end
end

module:hook("presence/bare", mod_remove_member_on_exit_presence_handler);
