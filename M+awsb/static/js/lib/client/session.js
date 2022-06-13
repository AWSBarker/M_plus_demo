"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const document_1 = require("../document");
const message_1 = require("../protocol/message");
const logging_1 = require("../core/logging");
class ClientSession {
    constructor(_connection, document, id) {
        this._connection = _connection;
        this.document = document;
        this.id = id;
        this._document_listener = (event) => this._document_changed(event);
        this.document.on_change(this._document_listener);
        this.event_manager = this.document.event_manager;
        this.event_manager.session = this;
    }
    handle(message) {
        const msgtype = message.msgtype();
        if (msgtype === 'PATCH-DOC')
            this._handle_patch(message);
        else if (msgtype === 'OK')
            this._handle_ok(message);
        else if (msgtype === 'ERROR')
            this._handle_error(message);
        else
            logging_1.logger.debug(`Doing nothing with message ${message.msgtype()}`);
    }
    close() {
        this._connection.close();
    }
    send_event(event) {
        const message = message_1.Message.create('EVENT', {}, JSON.stringify(event.to_json()));
        this._connection.send(message);
    }
    /*protected*/ _connection_closed() {
        this.document.remove_on_change(this._document_listener);
    }
    // Sends a request to the server for info about the server, such as its Bokeh
    // version. Returns a promise, the value of the promise is a free-form dictionary
    // of server details.
    request_server_info() {
        const message = message_1.Message.create('SERVER-INFO-REQ', {});
        const promise = this._connection.send_with_reply(message);
        return promise.then((reply) => reply.content);
    }
    // Sends some request to the server (no guarantee about which one) and returns
    // a promise which is completed when the server replies. The purpose of this
    // is that if you wait for the promise to be completed, you know the server
    // has processed the request. This is useful when writing tests because once
    // the server has processed this request it should also have processed any
    // events or requests you sent previously, which means you can check for the
    // results of that processing without a race condition. (This assumes the
    // server processes events in sequence, which it mostly has to semantically,
    // since reordering events might change the final state.)
    force_roundtrip() {
        return this.request_server_info().then((_) => undefined);
    }
    _document_changed(event) {
        // Filter out events that were initiated by the ClientSession itself
        if (event.setter_id === this.id) // XXX: not all document events define this
            return;
        // Filter out changes to attributes that aren't server-visible
        if (event instanceof document_1.ModelChangedEvent && !(event.attr in event.model.serializable_attributes()))
            return;
        // TODO (havocp) the connection may be closed here, which will
        // cause this send to throw an error - need to deal with it more cleanly.
        const message = message_1.Message.create('PATCH-DOC', {}, this.document.create_json_patch([event]));
        this._connection.send(message);
    }
    _handle_patch(message) {
        this.document.apply_json_patch(message.content, message.buffers, this.id);
    }
    _handle_ok(message) {
        logging_1.logger.trace(`Unhandled OK reply to ${message.reqid()}`);
    }
    _handle_error(message) {
        logging_1.logger.error(`Unhandled ERROR reply to ${message.reqid()}: ${message.content.text}`);
    }
}
exports.ClientSession = ClientSession;
ClientSession.__name__ = "ClientSession";
