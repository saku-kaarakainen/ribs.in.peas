-- NOTE: This script doesn't work and should be deleted. Please delete this.
USE mysqlkikbot;

SET @jid = 'testi';
SET @phr = 'FISHERMAN';

IF NOT EXISTS(SELECT gc.group_jid FROM group_chat gc WHERE gc.group_jid = @jid) THEN
	INSERT INTO group_chat(group_jid) VALUES (@jid);
END IF;

INSERT INTO group_chat_illegal_phrases(
	group_chat_id, phrase_text
) SELECT
	gc.id, @phr
FROM group_chat gc
WHERE gc.group_jid = @jid