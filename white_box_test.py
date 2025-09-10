import pytest
import pygame
from main import Player, Ghost, level, TILEWIDTH, TILEHEIGHT, NUMBERCOLS, NUMBERROWS, check_level_complete, reset_level, increase_speed
from board import boards as original_boards

@pytest.fixture
def game_setup():
    """A pytest fixture to set up a clean game state for each white-box test."""
    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    # Create a fresh, mutable copy of the level for each test.
    import main
    main.level = [row.copy() for row in original_boards]

    # Setup player
    player = Player(screen, 18, 15, 18 * TILEWIDTH, 15 * TILEHEIGHT, 0, 0, [], 0, False, 0, 7)
    main.player = player

    # Setup ghosts
    ghost_sprites = [pygame.Surface((1, 1))] * 6  # Dummy sprites
    ghosts = [
        Ghost(screen, 2, 2, 2 * TILEWIDTH, 2 * TILEHEIGHT, 0, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 2, 27, 27 * TILEWIDTH, 2 * TILEHEIGHT, 1, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 30, 2, 2 * TILEWIDTH, 30 * TILEHEIGHT, 2, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 30, 27, 27 * TILEWIDTH, 30 * TILEHEIGHT, 3, player, False, False, ghost_sprites, 0, 8)
    ]
    main.ghosts = ghosts

    yield player, ghosts, main.level

    pygame.quit()

def test_checkturns_in_open_space(game_setup):
    """Verify that in an open intersection, all four turns are allowed."""
    player, _, _ = game_setup
    # Position the player in an open intersection (e.g., row 22, col 15)
    player._Object__row, player._Object__col = 22, 15
    turns = player.checkTurns()
    assert turns == [True, True, True, True]

def test_checkturns_against_wall(game_setup):
    """Verify that moving towards a wall is correctly disallowed."""
    player, _, _ = game_setup
    # Position the player left of a vertical wall segment (row 23, col 2)
    player._Object__row, player._Object__col = 23, 2
    turns = player.checkTurns()
    # Expected: [Right: True, Left: False, Up: True, Down: True]
    assert turns == [True, False, True, True]

def test_player_move_counter_logic(game_setup):
    """Verify the player only moves after the move_counter reaches player_speed."""
    player, _, _ = game_setup
    player.player_speed = 5
    player.move_counter = 0
    player._Object__row, player._Object__col = 22, 15 # Open space
    player.direction_command = 0 # Move right
    initial_col = player.readCol()

    # Simulate 4 frames/calls, player should not move
    for _ in range(4):
        player.movePlayer()
    assert player.readCol() == initial_col

    # 5th call, player should move
    player.movePlayer()
    assert player.readCol() == initial_col + 1
    assert player.move_counter == 0 # Counter should reset

def test_powerup_duration(game_setup):
    """Verify the power-up state correctly expires after its duration (600 frames)."""
    player, _, _ = game_setup
    player.power = True
    player.power_counter = 599 # Set counter just before expiry

    player.powerUp()
    assert player.power is True # Should still be active

    player.powerUp()
    assert player.power is False # Should expire
    assert player.power_counter == 0 # Counter should reset

def test_ghost_clyde_behavior_when_close(game_setup):
    """White-box test for Ghost 3 (Clyde) AI.
    It should flee to its corner when within 8 tiles of the player."""
    player, ghosts, _ = game_setup
    clyde = ghosts[3]

    # Position player close to Clyde
    player._Object__row, player._Object__col = 28, 25
    clyde._Object__row, clyde._Object__col = 27, 26

    # Pathfind. Clyde should target its corner (30, 2), not the player.
    direction = clyde.findPath(player.readRow(), player.readCol())

    # Expected directions are down (3) or left (1) to move towards corner
    assert direction in [1, 3]

def test_ghost_fleeing_behavior_when_powered_up(game_setup):
    """Verify ghosts enter fleeing mode when the player is powered up."""
    player, ghosts, _ = game_setup
    player.power = True # Activate power-up
    blinky = ghosts[0] # Red ghost

    # Position player and ghost
    player._Object__row, player._Object__col = 20, 15
    blinky._Object__row, blinky._Object__col = 20, 18

    # Pathfind. Blinky should run away from the player towards its scatter corner (2, 2).
    direction = blinky.findPath(player.readRow(), player.readCol())

    # Expected directions are up (2) or left (1) to move away from player and towards corner
    assert direction in [1, 2]

def test_level_reset_on_completion(game_setup):
    """Verify that reset_level correctly restores the board and objects."""
    player, ghosts, test_level = game_setup
    import main

    # Modify the level and player/ghost state
    test_level[2][2] = 0 # "Eat" a pellet
    player._Object__row, player._Object__col = 10, 10
    ghosts[0]._Object__row, ghosts[0]._Object__col = 11, 11

    reset_level()

    # Check that the level is restored from the original boards
    assert main.level[2][2] == 1 # Pellet is back
    # Check that player and ghost positions are reset
    assert (player.readRow(), player.readCol()) == (18, 15)
    assert (ghosts[0].readRow(), ghosts[0].readCol()) == (2, 2)

def test_speed_increase_stops_at_minimum(game_setup):
    """Verify that speed values do not decrease below the minimum of 3."""
    import main
    # Set speeds to the minimum value
    main.player_speed = 3
    main.ghost_speed = 3

    increase_speed()

    # Assert that the speeds have not gone below the minimum
    assert main.player_speed == 3
    assert main.ghost_speed == 3