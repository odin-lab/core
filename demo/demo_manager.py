"""
Demo session manager that orchestrates microphone and recorder modules.
Shows how to use SessionManager from the base framework.
"""

import asyncio
import json
import logging
import sys
import uuid
from typing import Dict

from nats.aio.client import Client as NATS
from odin.nats.base import SessionManager

log = logging.getLogger(__name__)

# Module names must match what the modules register as
MODULES = ["microphone", "recorder"]


class DemoApp:
    """Interactive demo application for managing audio recording sessions."""
    
    def __init__(self, nats_url: str = "nats://127.0.0.1:9090"):
        self.nats_url = nats_url
        self.nc = None
        self.session_manager = None
        self.active_sessions: Dict[str, Dict] = {}
        
    async def connect(self):
        """Connect to NATS and initialize the session manager."""
        self.nc = NATS()
        await self.nc.connect(self.nats_url)
        
        # Initialize session manager with our modules
        self.session_manager = SessionManager(self.nc, MODULES)
        
        log.info(f"Connected to NATS at {self.nats_url}")
        
    async def start_session(self, session_name: str = None) -> str:
        """Start a new recording session."""
        # Generate session ID
        session_id = str(uuid.uuid4())
        if session_name:
            display_name = f"{session_name} ({session_id[:8]})"
        else:
            display_name = f"Session {session_id[:8]}"
        
        log.info(f"Starting {display_name}...")
        
        # Prepare module configurations
        configs = {
            "microphone": json.dumps({
                "sample_rate": 16000,
                "chunk_size": 1600
            }).encode(),
            "recorder": json.dumps({
                "output_dir": "recordings"
            }).encode()
        }
        
        try:
            # Start the session (this initializes both modules)
            await self.session_manager.start_session(session_id, configs, timeout=5.0)
            
            # Track active session
            self.active_sessions[session_id] = {
                "name": display_name,
                "started_at": asyncio.get_event_loop().time()
            }
            
            log.info(f"✅ {display_name} started successfully!")
            return session_id
            
        except Exception as e:
            log.error(f"Failed to start session: {e}")
            raise
    
    async def stop_session(self, session_id: str):
        """Stop a recording session."""
        if session_id not in self.active_sessions:
            log.error(f"Session {session_id} not found")
            return
            
        session_info = self.active_sessions[session_id]
        log.info(f"Stopping {session_info['name']}...")
        
        try:
            # Stop the session (this cleans up both modules)
            await self.session_manager.stop_session(session_id, timeout=5.0)
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            duration = asyncio.get_event_loop().time() - session_info['started_at']
            log.info(f"🛑 {session_info['name']} stopped (duration: {duration:.1f}s)")
            
        except Exception as e:
            log.error(f"Failed to stop session: {e}")
            raise
    
    async def list_sessions(self):
        """List all active sessions."""
        if not self.active_sessions:
            print("No active sessions")
            return
            
        print("\nActive sessions:")
        for sid, info in self.active_sessions.items():
            duration = asyncio.get_event_loop().time() - info['started_at']
            print(f"  - {info['name']} (running for {duration:.1f}s)")
    
    async def run_interactive(self):
        """Run interactive command-line interface."""
        print("\n🎙️  Audio Recording Session Manager")
        print("="*40)
        print("Commands:")
        print("  start [name]  - Start a new recording session")
        print("  stop <id>     - Stop a session by ID")
        print("  list          - List active sessions")
        print("  quit          - Exit the application")
        print("="*40)
        
        while True:
            try:
                # Get user input
                cmd_input = input("\n> ").strip().split()
                if not cmd_input:
                    continue
                    
                cmd = cmd_input[0].lower()
                args = cmd_input[1:]
                
                if cmd == "start":
                    name = " ".join(args) if args else None
                    session_id = await self.start_session(name)
                    print(f"Session ID: {session_id}")
                    
                elif cmd == "stop":
                    if not args:
                        print("Usage: stop <session_id>")
                        continue
                    
                    # Allow partial ID matching
                    target_id = args[0]
                    matching_ids = [sid for sid in self.active_sessions 
                                   if sid.startswith(target_id)]
                    
                    if len(matching_ids) == 0:
                        print(f"No session found matching '{target_id}'")
                    elif len(matching_ids) > 1:
                        print(f"Multiple sessions match '{target_id}':")
                        for sid in matching_ids:
                            print(f"  - {self.active_sessions[sid]['name']}")
                    else:
                        await self.stop_session(matching_ids[0])
                        
                elif cmd == "list":
                    await self.list_sessions()
                    
                elif cmd in ["quit", "exit", "q"]:
                    break
                    
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                log.error(f"Command failed: {e}")
    
    async def cleanup(self):
        """Clean up resources."""
        # Stop all active sessions
        for session_id in list(self.active_sessions.keys()):
            try:
                await self.stop_session(session_id)
            except Exception as e:
                log.error(f"Failed to stop session {session_id}: {e}")
        
        # Close NATS connection
        if self.nc:
            await self.nc.drain()


async def main():
    """Run the demo application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check command line arguments
    nats_url = "nats://127.0.0.1:9090"
    if len(sys.argv) > 1:
        nats_url = sys.argv[1]
    
    app = DemoApp(nats_url)
    
    try:
        await app.connect()
        
        print(f"\n⚠️  Make sure microphone and recorder modules are running!")
        print(f"Run these in separate terminals:")
        print(f"  python microphone_module.py")
        print(f"  python recorder_module.py")
        
        await app.run_interactive()
        
    except Exception as e:
        log.error(f"Application error: {e}")
    finally:
        await app.cleanup()
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    asyncio.run(main()) 