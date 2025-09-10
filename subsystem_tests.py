import pytest
import pygame
import main
from main import Player, Ghost, TILEWIDTH, TILEHEIGHT, check_level_complete
from board import boards as original_boards


def set_pos(obj, row, col):
    """Helper function to set both grid and pixel positions for a game object."""
    obj._Object__row = row
    obj._Object__col = col
    obj._Object__xPos = col * TILEWIDTH
    obj._Object__yPos = row * TILEHEIGHT


@pytest.fixture
def game_subsystem_setup(monkeypatch):
    """A pytest fixture to set up an integrated game environment for subsystem testing."""
    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    test_level = [row[:] for row in original_boards]
    monkeypatch.setattr(main, 'level', test_level)

    player_images = [pygame.Surface((1, 1))]
    player = Player(screen, 18, 15, 15 * TILEWIDTH, 18 * TILEHEIGHT, 0, 0, player_images, 0, False, 0, 7)
    monkeypatch.setattr(main, 'player', player)

    ghost_sprites = [pygame.Surface((1, 1))] * 6
    ghosts = [
        Ghost(screen, 2, 2, 2 * TILEWIDTH, 2 * TILEHEIGHT, 0, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 2, 27, 27 * TILEWIDTH, 2 * TILEHEIGHT, 1, player, False, False, ghost_sprites, 0, 8)
    ]
    monkeypatch.setattr(main, 'ghosts', ghosts)

    monkeypatch.setattr(main, 'player_speed', 7)
    monkeypatch.setattr(main, 'ghost_speed', 8)

    yield player, ghosts, test_level

    pygame.quit()


def test_player_eats_pellet_and_scores(game_subsystem_setup):
    """Test the subsystem interaction of player movement, collision, scoring, and level state change."""
    player, _, level = game_subsystem_setup

    # Arrange: Place player directly on a pellet at (2, 2).
    set_pos(player, 2, 2)
    initial_points = player.points
    assert level[2][2] == 1

    # Act: Check for collisions at the new position.
    player.checkCollisions()

    # Assert: Player's score increases and the pellet is removed from the level.
    assert player.points == initial_points + 1
    assert level[2][2] == 0


def test_full_powerup_ghost_eat_sequence(game_subsystem_setup):
    """Test the subsystem for eating a power pellet, which changes ghost AI, and then eating a ghost."""
    player, ghosts, level = game_subsystem_setup
    blinky = ghosts[0]
    initial_points = player.points

    # Arrange 1: Place player on a power pellet at (4, 2) and a ghost nearby.
    set_pos(player, 4, 2)
    set_pos(blinky, 4, 4)
    assert level[4][2] == 2

    # Act 1: Player eats the power pellet.
    player.checkCollisions()

    # Assert 1: Player is powered up, score increases, and pellet is gone.
    assert player.power is True
    assert player.points == initial_points + 10
    assert level[4][2] == 0

    # Arrange 2: Move player onto the ghost's position and create rects for collision.
    set_pos(player, 4, 4)
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    blinky.rect = pygame.Rect(blinky.readCentreXPos() - 18, blinky.readCentreYPos() - 18, 36, 36)

    # Act 2: Player collides with the ghost.
    player.checkGhostCollisions()

    # Assert 2: Ghost is eaten, score increases, and ghost is marked as mortal and sent to its corner.
    assert player.eaten_ghosts[0] is True
    assert player.points == initial_points + 10 + 100
    assert blinky.mortality is True
    assert (blinky.readRow(), blinky.readCol()) == (2, 2)


def test_level_completion_resets_and_increases_speed(game_subsystem_setup):
    """Test the subsystem for completing a level, which should reset entities and increase game speed."""
    player, ghosts, level = game_subsystem_setup

    # Arrange: Clear the board of all pellets except one.
    for r in range(len(level)):
        for c in range(len(level[r])):
            if level[r][c] in [1, 2]:
                level[r][c] = 0
    level[2][2] = 1  # Place one last pellet.
    set_pos(player, 2, 2)

    # Act: Player eats the last pellet, then we check if the level is complete.
    player.checkCollisions()
    level_is_complete = check_level_complete()

    # Assert
    assert level_is_complete is True

    # Verify effects of reset_level() and increase_speed() which are called by check_level_complete()
    # 1. Speeds are increased (values are decreased)
    assert player.player_speed == 6
    for ghost in ghosts:
        assert ghost.speed == 7

    # 2. Level board is reset. Check game.level directly as the local 'level' is now stale.
    assert main.level[2][3] == 1

    # 3. Player and ghosts are reset to their starting positions
    assert (player.readRow(), player.readCol()) == (18, 15)
    assert (ghosts[0].readRow(), ghosts[0].readCol()) == (2, 2)
    assert (ghosts[1].readRow(), ghosts[1].readCol()) == (2, 27)