import time
from datetime import datetime

def pomodoro_timer(work_mins=25, break_mins=5, cycles=4):
    """
    Pomodoro productivity timer.
    
    Args:
        work_mins: Minutes to work (default: 25)
        break_mins: Minutes for break (default: 5)
        cycles: Number of cycles (default: 4)
    """
    
    for cycle in range(1, cycles + 1):
        print(f"\n🔴 Cycle {cycle}/{cycles} - Work Time ({work_mins} mins)")
        print(f"Start: {datetime.now().strftime('%H:%M:%S')}")
        countdown(work_mins * 60)
        
        print(f"\n✅ Work complete! Break time ({break_mins} mins)")
        countdown(break_mins * 60)
    
    print("\n🎉 All cycles completed! Great work!")

def countdown(seconds):
    """Display countdown timer."""
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        print(f"\r⏱️  {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
        seconds -= 1
    print()

if __name__ == "__main__":
    pomodoro_timer(work_mins=25, break_mins=5, cycles=4)